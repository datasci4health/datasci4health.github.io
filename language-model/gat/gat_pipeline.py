"""
GAT Pipeline for Regulatory Networks
======================================
Computes Graph Attention Network (GAT) embeddings and attention weights for
a biological regulatory network containing genes, functional units, and miRNAs.

Inputs (CSV):
  nodes.csv          — node catalogue  (id, type, logic)
  edges.csv          — edge list        (source, target, type, subtype)
  gene_sequence.csv  — protein-coding sequences (id, sequence)
  mir_sequence.csv   — miRNA sequences          (id, sequence)

Outputs (CSV, written to --output-dir):
  node_embeddings.csv     — final node embeddings after GAT layers
  attention_weights.csv   — per-edge attention weights per GAT layer
  node_metadata.csv       — original node fields + assigned integer index
  edge_metadata.csv       — original edge fields + computed attention summary

Usage:
  python gat_pipeline.py \
      --nodes      data/nodes.csv \
      --edges      data/edges.csv \
      --gene-seq   data/gene_sequence.csv \
      --mir-seq    data/mir_sequence.csv \
      --output-dir results/

Architecture:
  1. Feature initialisation
       • Genes/functional-units  → amino-acid k-mer frequency vector (k=3)
       • miRNAs                  → RNA k-mer frequency vector (k=3)
       • All vectors projected to a common dimension via a linear layer
  2. GAT layers (configurable, default = 2)
       • Multi-head attention (default heads = 4)
       • Message passing over the directed edge list
       • Logic-aware aggregation: AND nodes use weighted mean of top-k
         neighbours; OR nodes use standard softmax-weighted sum
  3. Output
       • Node embeddings after each layer
       • α attention coefficients per edge per layer per head
"""

import argparse
import math
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# 1. Command-line interface
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="GAT pipeline for regulatory networks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--nodes",      required=True, help="Path to nodes.csv")
    p.add_argument("--edges",      required=True, help="Path to edges.csv")
    p.add_argument("--gene-seq",   required=True, help="Path to gene_sequence.csv")
    p.add_argument("--mir-seq",    required=True, help="Path to mir_sequence.csv")
    p.add_argument("--output-dir", default="results", help="Directory for output CSVs")
    p.add_argument("--embed-dim",  type=int, default=64,  help="Common embedding dimension")
    p.add_argument("--num-heads",  type=int, default=4,   help="Number of attention heads")
    p.add_argument("--num-layers", type=int, default=2,   help="Number of GAT layers")
    p.add_argument("--kmer",       type=int, default=3,   help="k for k-mer features")
    p.add_argument("--topk-and",   type=int, default=3,
                   help="Top-k neighbours used in AND-logic aggregation")
    p.add_argument("--seed",       type=int, default=42,  help="Random seed")
    return p.parse_args()


# ---------------------------------------------------------------------------
# 2. k-mer feature extraction
# ---------------------------------------------------------------------------

AA_ALPHABET  = list("ACDEFGHIKLMNPQRSTVWY")    # 20 standard amino acids
RNA_ALPHABET = list("ACGU")                     # 4 RNA bases

def build_kmer_vocab(alphabet: list[str], k: int) -> dict[str, int]:
    """Return a mapping from every length-k string over `alphabet` to an index."""
    return {"".join(t): i for i, t in enumerate(product(alphabet, repeat=k))}

def kmer_freq_vector(sequence: str, vocab: dict[str, int], k: int) -> np.ndarray:
    """Normalised k-mer frequency vector for a single sequence."""
    vec = np.zeros(len(vocab), dtype=np.float32)
    seq = sequence.upper()
    total = max(len(seq) - k + 1, 1)
    for i in range(len(seq) - k + 1):
        km = seq[i:i + k]
        if km in vocab:
            vec[vocab[km]] += 1
    vec /= total
    return vec


# ---------------------------------------------------------------------------
# 3. Data loading and graph construction
# ---------------------------------------------------------------------------

def load_data(
    nodes_path: str,
    edges_path: str,
    gene_seq_path: str,
    mir_seq_path: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    nodes   = pd.read_csv(nodes_path)
    edges   = pd.read_csv(edges_path)
    gene_seq = pd.read_csv(gene_seq_path)
    mir_seq  = pd.read_csv(mir_seq_path)

    required_node_cols = {"id", "type"}
    required_edge_cols = {"source", "target", "type", "subtype"}
    if not required_node_cols.issubset(nodes.columns):
        sys.exit(f"nodes.csv must contain columns: {required_node_cols}")
    if not required_edge_cols.issubset(edges.columns):
        sys.exit(f"edges.csv must contain columns: {required_edge_cols}")

    valid_types = {"gene", "functional_unit", "mir"}
    unknown = set(nodes["type"].unique()) - valid_types
    if unknown:
        sys.exit(f"Unknown node types: {unknown}. Expected: {valid_types}")

    return nodes, edges, gene_seq, mir_seq


def build_feature_matrix(
    nodes: pd.DataFrame,
    gene_seq: pd.DataFrame,
    mir_seq: pd.DataFrame,
    kmer_k: int,
) -> tuple[np.ndarray, dict]:
    """
    Build raw feature matrix X  (shape: N × raw_dim).

    • gene / functional_unit nodes  → AA 3-mer frequency (len 20^k)
    • mir nodes                     → RNA 3-mer frequency (len 4^k)

    Because the two feature spaces have different dimensions we zero-pad
    the shorter one so all rows share the same raw_dim.
    """
    aa_vocab  = build_kmer_vocab(AA_ALPHABET,  kmer_k)
    rna_vocab = build_kmer_vocab(RNA_ALPHABET, kmer_k)

    aa_dim  = len(aa_vocab)   # 20^k
    rna_dim = len(rna_vocab)  # 4^k
    raw_dim = aa_dim + rna_dim

    gene_seq_dict = dict(zip(gene_seq["id"], gene_seq["sequence"]))
    mir_seq_dict  = dict(zip(mir_seq["id"],  mir_seq["sequence"]))

    node_list = nodes["id"].tolist()
    node_idx  = {nid: i for i, nid in enumerate(node_list)}
    N         = len(node_list)
    X         = np.zeros((N, raw_dim), dtype=np.float32)

    missing_seq = []
    for _, row in nodes.iterrows():
        nid  = row["id"]
        ntype = row["type"]
        i    = node_idx[nid]

        if ntype in ("gene", "functional_unit"):
            seq = gene_seq_dict.get(nid, "")
            if not seq:
                missing_seq.append(nid)
            else:
                X[i, :aa_dim] = kmer_freq_vector(seq, aa_vocab, kmer_k)

        elif ntype == "mir":
            seq = mir_seq_dict.get(nid, "")
            if not seq:
                missing_seq.append(nid)
            else:
                X[i, aa_dim:] = kmer_freq_vector(seq, rna_vocab, kmer_k)

    if missing_seq:
        print(
            f"  [warn] No sequence found for {len(missing_seq)} node(s); "
            f"they will use zero-vectors: {missing_seq[:5]}"
            + (" ..." if len(missing_seq) > 5 else "")
        )

    meta = {
        "node_idx": node_idx,
        "node_list": node_list,
        "aa_dim": aa_dim,
        "rna_dim": rna_dim,
        "raw_dim": raw_dim,
    }
    return X, meta


def build_edge_index(
    edges: pd.DataFrame,
    node_idx: dict[str, int],
) -> tuple[torch.Tensor, list[tuple]]:
    """
    Convert edge DataFrame to a PyTorch edge_index tensor (2 × E).
    Edges whose endpoints are not in node_idx are skipped with a warning.
    Returns (edge_index, list_of_valid_edge_dicts).
    """
    src_list, dst_list, valid_edges = [], [], []
    skipped = 0
    for _, row in edges.iterrows():
        s, t = row["source"], row["target"]
        if s not in node_idx or t not in node_idx:
            skipped += 1
            continue
        src_list.append(node_idx[s])
        dst_list.append(node_idx[t])
        valid_edges.append(row.to_dict())

    if skipped:
        print(f"  [warn] Skipped {skipped} edge(s) with unknown node IDs.")

    edge_index = torch.tensor([src_list, dst_list], dtype=torch.long)
    return edge_index, valid_edges


# ---------------------------------------------------------------------------
# 4. GAT model (pure PyTorch, no external GNN library required)
# ---------------------------------------------------------------------------

class GATLayer(nn.Module):
    """
    Single Graph Attention layer with multi-head attention.

    For each target node i the update is:

        h'_i = σ( Σ_j α_{ij} · W · h_j )

    where the attention coefficient is:

        e_{ij}  = LeakyReLU( aᵀ [W·h_i ‖ W·h_j] )
        α_{ij}  = softmax over neighbours j of i

    Logic-aware aggregation (applies to functional_unit nodes only):
        • OR  → standard softmax-weighted sum  (default for all nodes)
        • AND → weighted mean over the top-k highest-attention neighbours
    """

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        num_heads: int = 4,
        dropout: float = 0.1,
        negative_slope: float = 0.2,
        concat_heads: bool = True,
    ):
        super().__init__()
        self.in_dim    = in_dim
        self.out_dim   = out_dim
        self.num_heads = num_heads
        self.concat    = concat_heads
        self.head_dim  = out_dim // num_heads if concat_heads else out_dim

        # One linear projection per head  (W in the formula)
        self.W = nn.Linear(in_dim, self.head_dim * num_heads, bias=False)

        # Attention vector  a  (length 2 * head_dim, one per head)
        self.a = nn.Parameter(torch.empty(num_heads, 2 * self.head_dim))
        nn.init.xavier_uniform_(self.a.unsqueeze(0))

        self.leaky_relu = nn.LeakyReLU(negative_slope)
        self.dropout    = nn.Dropout(dropout)

    def forward(
        self,
        h: torch.Tensor,            # (N, in_dim)
        edge_index: torch.Tensor,   # (2, E)
        logic_mask_and: torch.Tensor | None = None,  # (N,) bool, True = AND node
        topk: int = 3,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Returns:
            h_new   (N, out_dim or num_heads * head_dim)
            alpha   (E, num_heads)  — attention weights per edge per head
        """
        N = h.size(0)
        E = edge_index.size(1)

        # Project all node features  →  (N, num_heads, head_dim)
        Wh = self.W(h).view(N, self.num_heads, self.head_dim)

        src, dst = edge_index[0], edge_index[1]   # (E,) each

        # Gather src/dst projections for every edge
        Wh_src = Wh[src]   # (E, H, head_dim)
        Wh_dst = Wh[dst]   # (E, H, head_dim)

        # Attention score  e_{src→dst}
        cat = torch.cat([Wh_src, Wh_dst], dim=-1)  # (E, H, 2*head_dim)
        e = (cat * self.a.unsqueeze(0)).sum(dim=-1)  # (E, H)
        e = self.leaky_relu(e)

        # Softmax over in-neighbours of each dst node
        alpha = self._softmax_by_dest(e, dst, N)   # (E, H)

        # Logic-aware aggregation  -------------------------------------------
        # Default: use the full softmax-weighted sum (OR semantics)
        # AND nodes: re-weight so only top-k neighbours (per head) contribute

        if logic_mask_and is not None and logic_mask_and.any():
            alpha = self._and_reweight(alpha, dst, N, logic_mask_and, topk)

        alpha = self.dropout(alpha)

        # Aggregate:  h'_i = Σ_j α_{ij} * (W·h_j)
        # alpha (E, H, 1) * Wh_src (E, H, head_dim) → weighted sum per head
        agg = torch.zeros(N, self.num_heads, self.head_dim, device=h.device)
        alpha_exp = alpha.unsqueeze(-1)               # (E, H, 1)
        weighted  = alpha_exp * Wh_src                # (E, H, head_dim)
        agg.scatter_add_(0, dst.view(-1, 1, 1).expand_as(weighted), weighted)

        if self.concat:
            h_new = agg.view(N, self.num_heads * self.head_dim)  # (N, out_dim)
        else:
            h_new = agg.mean(dim=1)                              # (N, head_dim)

        return F.elu(h_new), alpha   # alpha: (E, H)

    @staticmethod
    def _softmax_by_dest(
        e: torch.Tensor,       # (E, H)
        dst: torch.Tensor,     # (E,)
        N: int,
    ) -> torch.Tensor:
        """Scatter softmax: for each destination node, normalise over its sources."""
        H = e.size(1)
        e_max = torch.full((N, H), -1e9, device=e.device)
        e_max.scatter_reduce_(0, dst.unsqueeze(1).expand_as(e), e, reduce="amax", include_self=True)
        e_shifted = e - e_max[dst]           # numerical stability
        exp_e = e_shifted.exp()
        denom = torch.zeros(N, H, device=e.device)
        denom.scatter_add_(0, dst.unsqueeze(1).expand_as(exp_e), exp_e)
        alpha = exp_e / (denom[dst] + 1e-16)
        return alpha

    @staticmethod
    def _and_reweight(
        alpha: torch.Tensor,         # (E, H)
        dst: torch.Tensor,           # (E,)
        N: int,
        logic_mask_and: torch.Tensor,  # (N,) bool
        topk: int,
    ) -> torch.Tensor:
        """
        For AND-logic nodes zero out all but the top-k attention weights
        (per head), then re-normalise so they sum to 1.
        This models conjunctive activation: the node integrates only its
        most strongly attended neighbours.
        """
        alpha_out = alpha.clone()
        H = alpha.size(1)

        and_nodes = logic_mask_and.nonzero(as_tuple=True)[0]  # indices of AND nodes
        for node in and_nodes.tolist():
            mask = (dst == node)
            if not mask.any():
                continue
            a_node = alpha_out[mask]          # (k_neighbors, H)
            k = min(topk, a_node.size(0))
            _, top_idx = a_node.topk(k, dim=0)

            new_a = torch.zeros_like(a_node)
            for h in range(H):
                top_vals = a_node[top_idx[:, h], h]
                new_a[top_idx[:, h], h] = top_vals / (top_vals.sum() + 1e-16)

            alpha_out[mask] = new_a

        return alpha_out


class GATModel(nn.Module):
    """Stack of GATLayer modules with a linear input projection."""

    def __init__(
        self,
        raw_dim: int,
        embed_dim: int,
        num_heads: int,
        num_layers: int,
    ):
        super().__init__()
        assert embed_dim % num_heads == 0, \
            f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})"

        self.input_proj = nn.Linear(raw_dim, embed_dim)

        self.gat_layers = nn.ModuleList(
            [GATLayer(embed_dim, embed_dim, num_heads) for _ in range(num_layers)]
        )
        self.num_layers = num_layers

    def forward(
        self,
        X: torch.Tensor,             # (N, raw_dim)
        edge_index: torch.Tensor,    # (2, E)
        logic_mask_and: torch.Tensor,  # (N,) bool
        topk_and: int,
    ) -> tuple[list[torch.Tensor], list[torch.Tensor]]:
        """
        Returns:
            layer_embeddings  — list of (N, embed_dim) tensors, one per layer
            layer_alphas      — list of (E, H) tensors, one per layer
        """
        h = F.elu(self.input_proj(X))    # (N, embed_dim)
        layer_embeddings = []
        layer_alphas     = []

        for gat in self.gat_layers:
            h, alpha = gat(h, edge_index, logic_mask_and, topk=topk_and)
            layer_embeddings.append(h)
            layer_alphas.append(alpha)

        return layer_embeddings, layer_alphas


# ---------------------------------------------------------------------------
# 5. Output helpers
# ---------------------------------------------------------------------------

def save_node_embeddings(
    layer_embeddings: list[torch.Tensor],
    node_list: list[str],
    output_dir: Path,
) -> None:
    """Save one CSV per GAT layer with shape (N, embed_dim)."""
    rows = []
    for layer_idx, emb in enumerate(layer_embeddings):
        arr = emb.detach().cpu().numpy()
        for node_id, vec in zip(node_list, arr):
            row = {"node_id": node_id, "layer": layer_idx + 1}
            row.update({f"dim_{j}": float(v) for j, v in enumerate(vec)})
            rows.append(row)

    df = pd.DataFrame(rows)
    path = output_dir / "node_embeddings.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}  ({len(df)} rows)")


def save_attention_weights(
    layer_alphas: list[torch.Tensor],
    valid_edges: list[dict],
    output_dir: Path,
) -> None:
    """
    Save attention weights per edge, per layer, per head.
    Also includes a mean_attention column averaged over heads.
    """
    rows = []
    for layer_idx, alpha in enumerate(layer_alphas):
        arr = alpha.detach().cpu().numpy()  # (E, H)
        num_heads = arr.shape[1]
        for edge_i, edge_dict in enumerate(valid_edges):
            row = {
                "layer":   layer_idx + 1,
                "source":  edge_dict["source"],
                "target":  edge_dict["target"],
                "edge_type":    edge_dict["type"],
                "edge_subtype": edge_dict["subtype"],
                "mean_attention": float(arr[edge_i].mean()),
            }
            for h in range(num_heads):
                row[f"head_{h+1}_attention"] = float(arr[edge_i, h])
            rows.append(row)

    df = pd.DataFrame(rows)
    path = output_dir / "attention_weights.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}  ({len(df)} rows)")


def save_node_metadata(
    nodes: pd.DataFrame,
    node_idx: dict[str, int],
    layer_embeddings: list[torch.Tensor],
    output_dir: Path,
) -> None:
    """
    Annotated node table: original columns + integer index +
    L2 norm of final-layer embedding (useful for ranking).
    """
    final_emb = layer_embeddings[-1].detach().cpu().numpy()
    df = nodes.copy()
    df.insert(0, "node_index", df["id"].map(node_idx))
    df["embedding_l2_norm"] = [
        float(np.linalg.norm(final_emb[node_idx[nid]])) for nid in df["id"]
    ]
    path = output_dir / "node_metadata.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}  ({len(df)} rows)")


def save_edge_metadata(
    valid_edges: list[dict],
    layer_alphas: list[torch.Tensor],
    output_dir: Path,
) -> None:
    """
    Edge table with final-layer mean attention and max-head attention,
    useful for quick downstream filtering.
    """
    final_alpha = layer_alphas[-1].detach().cpu().numpy()  # (E, H)
    rows = []
    for i, ed in enumerate(valid_edges):
        row = dict(ed)
        row["final_layer_mean_attn"] = float(final_alpha[i].mean())
        row["final_layer_max_attn"]  = float(final_alpha[i].max())
        rows.append(row)

    df = pd.DataFrame(rows)
    path = output_dir / "edge_metadata.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}  ({len(df)} rows)")


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Load ──────────────────────────────────────────────────────────────
    print("\n[1/5] Loading data …")
    nodes, edges, gene_seq, mir_seq = load_data(
        args.nodes, args.edges, args.gene_seq, args.mir_seq
    )
    print(f"  Nodes: {len(nodes)}  |  Edges: {len(edges)}")
    print(f"  Node types: {nodes['type'].value_counts().to_dict()}")
    print(f"  Edge subtypes: {edges['subtype'].value_counts().to_dict()}")

    # ── Features ──────────────────────────────────────────────────────────
    print(f"\n[2/5] Building {args.kmer}-mer feature matrix …")
    X_np, meta = build_feature_matrix(nodes, gene_seq, mir_seq, args.kmer)
    node_idx  = meta["node_idx"]
    node_list = meta["node_list"]
    print(f"  Raw feature dimension: {meta['raw_dim']}")
    print(f"  Feature matrix shape:  {X_np.shape}")

    X = torch.tensor(X_np)

    # ── Graph structure ────────────────────────────────────────────────────
    print("\n[3/5] Building edge index …")
    edge_index, valid_edges = build_edge_index(edges, node_idx)
    print(f"  Valid edges: {len(valid_edges)}")

    # Logic mask: True for AND-logic functional_unit nodes
    logic_series  = nodes.set_index("id")["logic"]
    logic_mask_and = torch.tensor(
        [
            (nodes.loc[nodes["id"] == nid, "type"].values[0] == "functional_unit")
            and (str(logic_series.get(nid, "OR")).strip().upper() == "AND")
            for nid in node_list
        ],
        dtype=torch.bool,
    )
    and_count = logic_mask_and.sum().item()
    print(f"  AND-logic nodes: {and_count}  |  OR-logic nodes: {len(node_list) - and_count}")

    # ── Model ─────────────────────────────────────────────────────────────
    print(f"\n[4/5] Running GAT  "
          f"(layers={args.num_layers}, heads={args.num_heads}, embed_dim={args.embed_dim}) …")

    model = GATModel(
        raw_dim    = meta["raw_dim"],
        embed_dim  = args.embed_dim,
        num_heads  = args.num_heads,
        num_layers = args.num_layers,
    )
    model.eval()   # no training — this is a forward-pass demonstration

    with torch.no_grad():
        layer_embeddings, layer_alphas = model(
            X, edge_index, logic_mask_and, topk_and=args.topk_and
        )

    for i, (emb, alp) in enumerate(zip(layer_embeddings, layer_alphas)):
        print(f"  Layer {i+1}: embeddings {tuple(emb.shape)}  "
              f"attention {tuple(alp.shape)}")

    # ── Save ──────────────────────────────────────────────────────────────
    print(f"\n[5/5] Writing results to '{output_dir}/' …")
    save_node_embeddings(layer_embeddings, node_list, output_dir)
    save_attention_weights(layer_alphas, valid_edges, output_dir)
    save_node_metadata(nodes, node_idx, layer_embeddings, output_dir)
    save_edge_metadata(valid_edges, layer_alphas, output_dir)

    print("\n✓ Pipeline complete.\n")


if __name__ == "__main__":
    main()
