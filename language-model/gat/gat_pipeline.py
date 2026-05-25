"""
GAT Pipeline for Regulatory Networks  (v2)
============================================
Computes Graph Attention Network (GAT) embeddings and per-edge attention
weights for a biological regulatory network of genes, functional units,
and miRNAs.

Node feature initialisation — three modes (--encoder flag):
  kmer        Pure k-mer frequency vectors (fast, no model download).
              Useful for a quick first run or when sequences are short.
  esm2        ESM-2 (facebook/esm2_t6_8M_UR50D) for protein sequences +
              k-mer for miRNAs.  Downloads ~30 MB on first run; runs on CPU
              in seconds per sequence.  Recommended for classroom use.
  proteinbert ProteinBERT-style tokenisation + a lightweight transformer
              encoder built in-house (no weight download needed). Produces
              richer protein representations than plain k-mer without the
              ESM-2 download. Good middle ground.

Inputs (CSV):
  nodes.csv          (id, type, logic)
  edges.csv          (source, target, type, subtype)
  gene_sequence.csv  (id, sequence)    — amino-acid sequences
  mir_sequence.csv   (id, sequence)    — RNA sequences (ACGU alphabet)

Outputs (CSV, --output-dir):
  node_embeddings.csv     final GAT embeddings per layer
  attention_weights.csv   per-edge α weights per layer per head
  node_metadata.csv       original node fields + embedding L2 norm
  edge_metadata.csv       original edge fields + final-layer attention
"""

import argparse, math, sys, warnings
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

warnings.filterwarnings("ignore", category=UserWarning)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="GAT pipeline for regulatory networks (v2)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--nodes",      required=True)
    p.add_argument("--edges",      required=True)
    p.add_argument("--gene-seq",   required=True)
    p.add_argument("--mir-seq",    required=True)
    p.add_argument("--output-dir", default="results")
    p.add_argument("--encoder",    default="kmer",
                   choices=["kmer", "esm2", "proteinbert"],
                   help=(
                       "kmer: fast k-mer vectors (baseline). "
                       "esm2: ESM-2 protein LM + k-mer for miRNA (recommended). "
                       "proteinbert: lightweight in-house protein encoder + k-mer for miRNA."
                   ))
    p.add_argument("--embed-dim",  type=int, default=64)
    p.add_argument("--num-heads",  type=int, default=4)
    p.add_argument("--num-layers", type=int, default=2)
    p.add_argument("--kmer",       type=int, default=3)
    p.add_argument("--topk-and",   type=int, default=3)
    p.add_argument("--seed",       type=int, default=42)
    return p.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# k-mer encoder (shared baseline for miRNAs and kmer-mode proteins)
# ─────────────────────────────────────────────────────────────────────────────

AA_ALPHABET  = list("ACDEFGHIKLMNPQRSTVWY")
RNA_ALPHABET = list("ACGU")

def build_kmer_vocab(alphabet, k):
    return {"".join(t): i for i, t in enumerate(product(alphabet, repeat=k))}

def kmer_freq(seq, vocab, k):
    vec = np.zeros(len(vocab), dtype=np.float32)
    seq = seq.upper()
    total = max(len(seq) - k + 1, 1)
    for i in range(len(seq) - k + 1):
        km = seq[i:i+k]
        if km in vocab:
            vec[vocab[km]] += 1
    vec /= total
    return vec

def normalise_node_type(node_type):
    value = str(node_type).strip().lower()
    if value in {"mir", "mirna", "microrna", "micro_rna", "micro-rna"}:
        return "mir"
    if value in {"gene", "mrna", "protein"}:
        return "gene"
    if value in {"functional_unit", "functional unit", "fu"}:
        return "functional_unit"
    return value

def build_sequence_dict(seq_df):
    return {
        str(row["id"]).strip(): str(row["sequence"]).strip()
        for _, row in seq_df.dropna(subset=["id", "sequence"]).iterrows()
    }


# ─────────────────────────────────────────────────────────────────────────────
# Lightweight in-house ProteinBERT-style encoder
#   • character-level tokenisation over the 20 AA alphabet
#   • sinusoidal position encoding
#   • 2-layer transformer encoder
#   • mean-pool → final protein vector
# ─────────────────────────────────────────────────────────────────────────────

class LightweightProteinEncoder(nn.Module):
    AA_VOCAB = {aa: i+1 for i, aa in enumerate("ACDEFGHIKLMNPQRSTVWY")}
    PAD = 0
    MAX_LEN = 512

    def __init__(self, embed_dim=128, nhead=4, num_layers=2):
        super().__init__()
        vocab_size = len(self.AA_VOCAB) + 1   # +1 for PAD
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=self.PAD)
        self.pos_enc = self._sinusoidal(self.MAX_LEN, embed_dim)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=nhead, dim_feedforward=embed_dim*4,
            dropout=0.0, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(enc_layer, num_layers=num_layers)
        self.out_dim = embed_dim

    @staticmethod
    def _sinusoidal(max_len, d):
        pe = torch.zeros(max_len, d)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, d, 2).float() * (-math.log(10000.0) / d))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        return pe  # (max_len, d)

    def tokenise(self, seq):
        seq = seq.upper()[:self.MAX_LEN]
        return [self.AA_VOCAB.get(aa, self.PAD) for aa in seq]

    @torch.no_grad()
    def encode(self, sequences):
        """Encode a list of AA sequences → (N, embed_dim) numpy array."""
        tokens  = [self.tokenise(s) for s in sequences]
        maxlen  = max(len(t) for t in tokens)
        ids     = torch.zeros(len(tokens), maxlen, dtype=torch.long)
        pad_mask= torch.ones(len(tokens), maxlen, dtype=torch.bool)  # True=ignore
        for i, t in enumerate(tokens):
            ids[i, :len(t)] = torch.tensor(t)
            pad_mask[i, :len(t)] = False

        x = self.embed(ids)                              # (N, L, d)
        pe = self.pos_enc[:maxlen].unsqueeze(0)          # (1, L, d)
        x = x + pe
        x = self.transformer(x, src_key_padding_mask=pad_mask)
        # mean-pool over non-padded positions
        mask_f = (~pad_mask).float().unsqueeze(-1)       # (N, L, 1)
        emb = (x * mask_f).sum(1) / mask_f.sum(1).clamp(min=1)
        return emb.cpu().numpy()


# ─────────────────────────────────────────────────────────────────────────────
# ESM-2 encoder (facebook/esm2_t6_8M_UR50D — smallest model, ~30 MB)
# ─────────────────────────────────────────────────────────────────────────────

def load_esm2():
    try:
        from transformers import AutoTokenizer, AutoModel
        name = "facebook/esm2_t6_8M_UR50D"
        print(f"    Loading ESM-2 ({name}) …")
        tok = AutoTokenizer.from_pretrained(name)
        mdl = AutoModel.from_pretrained(name)
        mdl.eval()
        return tok, mdl
    except Exception as e:
        sys.exit(
            f"Could not load ESM-2 via HuggingFace transformers: {e}\n"
            "Install with:  pip install transformers\n"
            "Or use --encoder kmer to run without a protein language model."
        )

@torch.no_grad()
def esm2_encode(sequences, tokenizer, model, batch_size=8):
    """Encode AA sequences with ESM-2 (mean-pool over residues)."""
    all_emb = []
    for i in range(0, len(sequences), batch_size):
        batch = sequences[i:i+batch_size]
        enc   = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        out   = model(**enc)
        # mean-pool last hidden state over real (non-padding) positions
        mask  = enc["attention_mask"].unsqueeze(-1).float()
        emb   = (out.last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1)
        all_emb.append(emb.cpu().numpy())
    return np.vstack(all_emb)


# ─────────────────────────────────────────────────────────────────────────────
# Feature matrix builder
# ─────────────────────────────────────────────────────────────────────────────

def build_feature_matrix(nodes, gene_seq, mir_seq, kmer_k, encoder_mode):
    """
    Returns (X: np.ndarray shape N×raw_dim, meta: dict).
    raw_dim = protein_dim + rna_dim  (rna_dim is always k-mer based)
    """
    gene_seq_dict = build_sequence_dict(gene_seq)
    mir_seq_dict  = build_sequence_dict(mir_seq)

    node_list = [str(nid).strip() for nid in nodes["id"].tolist()]
    node_idx  = {nid: i for i, nid in enumerate(node_list)}
    N         = len(node_list)
    node_types = {
        str(row["id"]).strip(): normalise_node_type(row["type"])
        for _, row in nodes.iterrows()
    }

    rna_vocab = build_kmer_vocab(RNA_ALPHABET, kmer_k)
    rna_dim   = len(rna_vocab)

    # ── choose protein encoder ────────────────────────────────────────────
    print(f"  Encoder mode: {encoder_mode}")

    if encoder_mode == "kmer":
        aa_vocab  = build_kmer_vocab(AA_ALPHABET, kmer_k)
        prot_dim  = len(aa_vocab)
        prot_encoder = None
        esm_tok = esm_mdl = None

    elif encoder_mode == "esm2":
        esm_tok, esm_mdl = load_esm2()
        prot_dim = esm_mdl.config.hidden_size
        aa_vocab  = None
        prot_encoder = None

    elif encoder_mode == "proteinbert":
        prot_dim = 128
        prot_encoder = LightweightProteinEncoder(embed_dim=prot_dim, nhead=4, num_layers=2)
        prot_encoder.eval()
        aa_vocab  = None
        esm_tok = esm_mdl = None

    raw_dim = prot_dim + rna_dim
    X = np.zeros((N, raw_dim), dtype=np.float32)

    # split nodes by type
    mir_node_ids = [nid for nid in node_list if node_types.get(nid) == "mir"]
    prot_ids = [nid for nid in node_list
                if node_types.get(nid) in ("gene","functional_unit")
                and gene_seq_dict.get(nid,"")]
    mir_ids  = [nid for nid in node_list
                if node_types.get(nid) == "mir"
                and mir_seq_dict.get(nid,"")]
    missing_mir_ids = [nid for nid in mir_node_ids if nid not in mir_ids]
    missing  = [nid for nid in node_list
                if nid not in prot_ids and nid not in mir_ids]
    if missing:
        print(f"  [warn] No sequence for {len(missing)} node(s) → zero-vector: {missing[:5]}"
              + (" ..." if len(missing)>5 else ""))
    if missing_mir_ids:
        print(f"  [warn] No miRNA sequence for {len(missing_mir_ids)} miR node(s); "
              f"expected matching IDs in --mir-seq. Examples: {missing_mir_ids[:5]}"
              + (" ..." if len(missing_mir_ids)>5 else ""))

    # ── encode proteins ───────────────────────────────────────────────────
    if prot_ids:
        seqs = [gene_seq_dict[nid] for nid in prot_ids]

        if encoder_mode == "kmer":
            for nid, seq in zip(prot_ids, seqs):
                X[node_idx[nid], :prot_dim] = kmer_freq(seq, aa_vocab, kmer_k)

        elif encoder_mode == "esm2":
            print(f"  Running ESM-2 on {len(prot_ids)} protein sequence(s) …")
            embs = esm2_encode(seqs, esm_tok, esm_mdl)
            for nid, emb in zip(prot_ids, embs):
                X[node_idx[nid], :prot_dim] = emb

        elif encoder_mode == "proteinbert":
            print(f"  Running lightweight ProteinBERT on {len(prot_ids)} sequence(s) …")
            embs = prot_encoder.encode(seqs)
            for nid, emb in zip(prot_ids, embs):
                X[node_idx[nid], :prot_dim] = emb

    # ── encode miRNAs (always k-mer) ──────────────────────────────────────
    if mir_ids:
        print(f"  Encoding {len(mir_ids)} miRNA sequence(s) with RNA k-mer …")
    for nid in mir_ids:
        seq = mir_seq_dict[nid].upper().replace("T","U")
        X[node_idx[nid], prot_dim:] = kmer_freq(seq, rna_vocab, kmer_k)

    meta = dict(node_idx=node_idx, node_list=node_list,
                prot_dim=prot_dim, rna_dim=rna_dim, raw_dim=raw_dim)
    return X, meta


# ─────────────────────────────────────────────────────────────────────────────
# Graph construction
# ─────────────────────────────────────────────────────────────────────────────

def build_edge_index(edges, node_idx, add_self_loops=True):
    src_list, dst_list, valid = [], [], []
    skipped = 0
    for _, row in edges.iterrows():
        s, t = str(row["source"]).strip(), str(row["target"]).strip()
        if s not in node_idx or t not in node_idx:
            skipped += 1; continue
        src_list.append(node_idx[s]); dst_list.append(node_idx[t])
        ed = row.to_dict()
        ed["source"] = s
        ed["target"] = t
        valid.append(ed)
    if add_self_loops:
        for nid, idx in node_idx.items():
            src_list.append(idx)
            dst_list.append(idx)
            valid.append({
                "source": nid,
                "target": nid,
                "type": "self_loop",
                "subtype": "self_loop",
            })
    if skipped:
        print(f"  [warn] Skipped {skipped} edge(s) with unknown node IDs.")
    return torch.tensor([src_list, dst_list], dtype=torch.long), valid


# ─────────────────────────────────────────────────────────────────────────────
# GAT model
# ─────────────────────────────────────────────────────────────────────────────

class GATLayer(nn.Module):
    def __init__(self, in_dim, out_dim, num_heads=4, dropout=0.1, negative_slope=0.2):
        super().__init__()
        self.H  = num_heads
        self.hd = out_dim // num_heads
        self.W  = nn.Linear(in_dim, self.hd * num_heads, bias=False)
        self.a  = nn.Parameter(torch.empty(num_heads, 2 * self.hd))
        nn.init.xavier_uniform_(self.a.unsqueeze(0))
        self.lrelu   = nn.LeakyReLU(negative_slope)
        self.dropout = nn.Dropout(dropout)

    def forward(self, h, edge_index, logic_mask_and, topk):
        N = h.size(0)
        src, dst = edge_index[0], edge_index[1]

        Wh = self.W(h).view(N, self.H, self.hd)
        cat = torch.cat([Wh[src], Wh[dst]], dim=-1)           # (E,H,2hd)
        e   = self.lrelu((cat * self.a.unsqueeze(0)).sum(-1))  # (E,H)

        alpha = self._softmax_by_dst(e, dst, N)

        if logic_mask_and is not None and logic_mask_and.any():
            alpha = self._and_reweight(alpha, dst, N, logic_mask_and, topk)

        alpha = self.dropout(alpha)

        agg = torch.zeros(N, self.H, self.hd, device=h.device)
        agg.scatter_add_(0, dst.view(-1,1,1).expand(-1,self.H,self.hd),
                         alpha.unsqueeze(-1) * Wh[src])

        return F.elu(agg.view(N, self.H * self.hd)), alpha

    @staticmethod
    def _softmax_by_dst(e, dst, N):
        H = e.size(1)
        e_max = torch.full((N,H), -1e9, device=e.device)
        e_max.scatter_reduce_(0, dst.unsqueeze(1).expand_as(e), e,
                              reduce="amax", include_self=True)
        exp_e = (e - e_max[dst]).exp()
        denom = torch.zeros(N,H,device=e.device)
        denom.scatter_add_(0, dst.unsqueeze(1).expand_as(exp_e), exp_e)
        return exp_e / (denom[dst] + 1e-16)

    @staticmethod
    def _and_reweight(alpha, dst, N, mask_and, topk):
        alpha_out = alpha.clone()
        H = alpha.size(1)
        for node in mask_and.nonzero(as_tuple=True)[0].tolist():
            m = (dst == node)
            if not m.any(): continue
            a_node = alpha_out[m]
            k = min(topk, a_node.size(0))
            _, top_idx = a_node.topk(k, dim=0)
            new_a = torch.zeros_like(a_node)
            for hd in range(H):
                tv = a_node[top_idx[:,hd], hd]
                new_a[top_idx[:,hd], hd] = tv / (tv.sum() + 1e-16)
            alpha_out[m] = new_a
        return alpha_out


class GATModel(nn.Module):
    def __init__(self, raw_dim, embed_dim, num_heads, num_layers):
        super().__init__()
        assert embed_dim % num_heads == 0
        self.input_proj = nn.Linear(raw_dim, embed_dim)
        self.layers = nn.ModuleList(
            [GATLayer(embed_dim, embed_dim, num_heads) for _ in range(num_layers)]
        )

    def forward(self, X, edge_index, logic_mask_and, topk_and):
        h = F.elu(self.input_proj(X))
        embs, alphas = [], []
        for layer in self.layers:
            h, alpha = layer(h, edge_index, logic_mask_and, topk_and)
            embs.append(h); alphas.append(alpha)
        return embs, alphas


# ─────────────────────────────────────────────────────────────────────────────
# Output writers
# ─────────────────────────────────────────────────────────────────────────────

def save_node_embeddings(layer_embs, node_list, out_dir):
    rows = []
    for li, emb in enumerate(layer_embs):
        arr = emb.detach().cpu().numpy()
        for nid, vec in zip(node_list, arr):
            row = {"node_id": nid, "layer": li+1}
            row.update({f"dim_{j}": float(v) for j,v in enumerate(vec)})
            rows.append(row)
    path = out_dir / "node_embeddings.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  Saved → {path}")

def save_attention_weights(layer_alphas, valid_edges, out_dir):
    rows = []
    for li, alpha in enumerate(layer_alphas):
        arr = alpha.detach().cpu().numpy()
        H   = arr.shape[1]
        for ei, ed in enumerate(valid_edges):
            row = {"layer": li+1, "source": ed["source"], "target": ed["target"],
                   "edge_type": ed["type"], "edge_subtype": ed["subtype"],
                   "mean_attention": float(arr[ei].mean())}
            for h in range(H):
                row[f"head_{h+1}_attention"] = float(arr[ei,h])
            rows.append(row)
    path = out_dir / "attention_weights.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  Saved → {path}")

def save_node_metadata(nodes, node_idx, layer_embs, encoder_mode, out_dir):
    final = layer_embs[-1].detach().cpu().numpy()
    df = nodes.copy()
    df.insert(0, "node_index", df["id"].map(node_idx))
    df["embedding_l2_norm"] = [float(np.linalg.norm(final[node_idx[nid]])) for nid in df["id"]]
    df["encoder"] = encoder_mode
    path = out_dir / "node_metadata.csv"
    df.to_csv(path, index=False)
    print(f"  Saved → {path}")

def save_edge_metadata(valid_edges, layer_alphas, out_dir):
    final = layer_alphas[-1].detach().cpu().numpy()
    rows = []
    for i, ed in enumerate(valid_edges):
        row = dict(ed)
        row["final_layer_mean_attn"] = float(final[i].mean())
        row["final_layer_max_attn"]  = float(final[i].max())
        rows.append(row)
    path = out_dir / "edge_metadata.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  Saved → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    torch.manual_seed(args.seed); np.random.seed(args.seed)
    out_dir = Path(args.output_dir); out_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1/5] Loading data …")
    nodes    = pd.read_csv(args.nodes)
    edges    = pd.read_csv(args.edges)
    gene_seq = pd.read_csv(args.gene_seq)
    mir_seq  = pd.read_csv(args.mir_seq)
    nodes["id"] = nodes["id"].astype(str).str.strip()
    edges["source"] = edges["source"].astype(str).str.strip()
    edges["target"] = edges["target"].astype(str).str.strip()
    gene_seq["id"] = gene_seq["id"].astype(str).str.strip()
    mir_seq["id"] = mir_seq["id"].astype(str).str.strip()
    print(f"  Nodes: {len(nodes)}  |  Edges: {len(edges)}")
    print(f"  Node types:   {nodes['type'].value_counts().to_dict()}")
    print(f"  Edge subtypes:{edges['subtype'].value_counts().to_dict()}")

    print(f"\n[2/5] Building feature matrix (encoder={args.encoder}) …")
    X_np, meta = build_feature_matrix(nodes, gene_seq, mir_seq, args.kmer, args.encoder)
    print(f"  Raw feature dim: {meta['raw_dim']}  "
          f"(protein={meta['prot_dim']}, RNA k-mer={meta['rna_dim']})")
    print(f"  Feature matrix : {X_np.shape}")
    X = torch.tensor(X_np)

    print("\n[3/5] Building edge index …")
    edge_index, valid_edges = build_edge_index(edges, meta["node_idx"])
    logic_series   = nodes.set_index("id")["logic"]
    node_type_series = nodes.set_index("id")["type"].map(normalise_node_type)
    logic_mask_and = torch.tensor([
        node_type_series.get(nid) == "functional_unit"
        and str(logic_series.get(nid,"OR")).strip().upper() == "AND"
        for nid in meta["node_list"]
    ], dtype=torch.bool)
    print(f"  Valid edges: {len(valid_edges)}")
    print(f"  AND-logic nodes: {logic_mask_and.sum().item()}")

    print(f"\n[4/5] Running GAT forward pass "
          f"(layers={args.num_layers}, heads={args.num_heads}, embed_dim={args.embed_dim}) …")

    # Note on training:
    # The GAT layers are NOT trained here — this is an unsupervised forward pass.
    # The node features (from the chosen encoder) carry the biological signal;
    # the GAT propagates that signal across the graph topology and produces
    # attention weights that reflect structural neighbourhood patterns.
    #
    # To train the GAT on a supervised signal (e.g. pathway membership or
    # disease association), add a classification head, define a loss function,
    # and call loss.backward() + an optimiser step before the save calls below.
    # Even a few epochs on CPU will produce biologically-informed attention weights.

    model = GATModel(meta["raw_dim"], args.embed_dim, args.num_heads, args.num_layers)
    model.eval()
    with torch.no_grad():
        layer_embs, layer_alphas = model(X, edge_index, logic_mask_and, args.topk_and)

    for i, (emb, alp) in enumerate(zip(layer_embs, layer_alphas)):
        print(f"  Layer {i+1}: embeddings {tuple(emb.shape)}  attention {tuple(alp.shape)}")

    print(f"\n[5/5] Writing results to '{out_dir}/' …")
    save_node_embeddings(layer_embs, meta["node_list"], out_dir)
    save_attention_weights(layer_alphas, valid_edges, out_dir)
    save_node_metadata(nodes, meta["node_idx"], layer_embs, args.encoder, out_dir)
    save_edge_metadata(valid_edges, layer_alphas, out_dir)

    print(f"\n✓ Pipeline complete (encoder={args.encoder}).\n")
    if args.encoder == "kmer":
        print("  Tip: re-run with --encoder esm2 to initialise protein node features")
        print("  from a pretrained protein language model (~30 MB download, CPU-friendly).\n")


if __name__ == "__main__":
    main()
