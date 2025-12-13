from lxml import etree
import pandas as pd
from collections import defaultdict
import uuid
import requests
import tempfile
import os


class KeggKgmlToNetwork:
    """
    Backward-compatible KEGG KGML → Functional Unit → Network extractor.

    Supports TWO MODES:
    1) Legacy mode:
       - Input: local KGML file
       - Output: flat CSV + Cytoscape CSVs

    2) Multi-pathway mode (g:Profiler-style):
       - Input: list of KEGG pathways + list of genes of interest
       - Output: merged, filtered network
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, kgml_path=None):
        self.kgml_path = kgml_path
        self.root = None
        self.functional_units = []

    # ------------------------------------------------------------------
    # KGML parsing (UNCHANGED)
    # ------------------------------------------------------------------

    def parse_kgml(self):
        if not self.kgml_path:
            raise ValueError("No KGML path provided.")
        tree = etree.parse(self.kgml_path)
        self.root = tree.getroot()
        return self.root

    @staticmethod
    def _parse_gene_names(name_field):
        if not name_field:
            return []
        return name_field.strip().split()

    # ------------------------------------------------------------------
    # Functional Unit extraction (UNCHANGED)
    # ------------------------------------------------------------------

    def extract_functional_units(self):
        if self.root is None:
            self.parse_kgml()

        entries = {}
        groups = {}
        pathway_id = self.root.attrib.get("name", "unknown_pathway")

        for entry in self.root.findall("entry"):
            entry_id = entry.attrib["id"]
            entries[entry_id] = {
                "entry_id": entry_id,
                "type": entry.attrib.get("type"),
                "name": entry.attrib.get("name"),
                "reaction": entry.attrib.get("reaction", "").split()
            }

        for entry in self.root.findall("entry"):
            if entry.attrib.get("type") == "group":
                groups[entry.attrib["id"]] = [
                    c.attrib["id"] for c in entry.findall("component")
                ]

        functional_units = []

        # --- AND logic (complexes) ---
        for group_id, component_ids in groups.items():
            genes, reactions = [], set()
            for cid in component_ids:
                comp = entries.get(cid)
                if comp and comp["type"] == "gene":
                    genes.extend(self._parse_gene_names(comp["name"]))
                    reactions.update(comp["reaction"])

            fu_id = f"FU_{uuid.uuid4().hex[:8]}"
            for target in reactions or [group_id]:
                functional_units.append(self._make_fu(
                    pathway_id, target, fu_id, "AND", genes, group_id,
                    "protein complex inferred from group"
                ))

        # --- SINGLE / OR logic ---
        for entry in entries.values():
            if entry["type"] != "gene":
                continue

            genes = self._parse_gene_names(entry["name"])
            if not genes:
                continue

            logic = "OR" if len(genes) > 1 else "SINGLE"
            fu_id = f"FU_{uuid.uuid4().hex[:8]}"
            targets = entry["reaction"] or [entry["entry_id"]]

            for target in targets:
                functional_units.append(self._make_fu(
                    pathway_id, target, fu_id, logic, genes,
                    entry["entry_id"],
                    "isozyme group" if logic == "OR" else ""
                ))

        self.functional_units = functional_units
        return functional_units

    def _make_fu(self, pathway_id, target, fu_id, logic, genes, entry_id, notes):
        return {
            "pathway_id": pathway_id,
            "pathway_position_id": target,
            "pathway_position_type": "reaction" if target.startswith("rn:") else "node",
            "functional_unit_id": fu_id,
            "functional_unit_logic": logic,
            "genes": genes,
            "entry_id": entry_id,
            "evidence": "KGML",
            "notes": notes
        }

    # ------------------------------------------------------------------
    # NEW: KEGG API KGML retrieval
    # ------------------------------------------------------------------

    @staticmethod
    def fetch_kgml_from_kegg(pathway_id):
        url = f"https://rest.kegg.jp/get/{pathway_id}/kgml"
        r = requests.get(url)
        if not r.ok:
            raise RuntimeError(f"Cannot retrieve KGML for {pathway_id}")
        return r.text

    # ------------------------------------------------------------------
    # NEW: Multi-pathway + gene list workflow
    # ------------------------------------------------------------------

    def build_from_pathway_and_gene_lists(self, pathway_ids, genes_of_interest):
        """
        High-level pipeline:
        1) Download KGMLs
        2) Extract FUs
        3) Merge graphs
        4) Filter genes
        5) Remove empty FUs
        """

        all_fus = []

        for pid in pathway_ids:
            kgml_text = self.fetch_kgml_from_kegg(pid)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(kgml_text.encode("utf-8"))
                tmp_path = tmp.name

            tmp_builder = KeggKgmlToNetwork(tmp_path)
            tmp_builder.extract_functional_units()
            all_fus.extend(tmp_builder.functional_units)

            os.unlink(tmp_path)

        merged = self._merge_functional_units(all_fus)
        filtered = self._filter_by_genes(merged, genes_of_interest)

        self.functional_units = filtered
        return filtered

    # ------------------------------------------------------------------
    # NEW: Graph merge logic
    # ------------------------------------------------------------------

    def _merge_functional_units(self, fus):
        merged = {}
        for fu in fus:
            key = (
                tuple(sorted(fu["genes"])),
                fu["pathway_position_id"],
                fu["functional_unit_logic"]
            )
            if key not in merged:
                merged[key] = fu
            else:
                merged[key]["pathway_id"] += f";{fu['pathway_id']}"
        return list(merged.values())

    # ------------------------------------------------------------------
    # NEW: Filtering
    # ------------------------------------------------------------------

    def _filter_by_genes(self, fus, genes_of_interest):
        genes_of_interest = set(genes_of_interest)
        filtered = []

        for fu in fus:
            kept_genes = [g for g in fu["genes"] if g in genes_of_interest]
            if kept_genes:
                fu = fu.copy()
                fu["genes"] = kept_genes
                filtered.append(fu)

        return filtered

    # ------------------------------------------------------------------
    # CSV exports (UNCHANGED)
    # ------------------------------------------------------------------

    def to_flat_dataframe(self):
        rows = []
        for fu in self.functional_units:
            for gene in fu["genes"]:
                rows.append({
                    "pathway_id": fu["pathway_id"],
                    "pathway_position_id": fu["pathway_position_id"],
                    "pathway_position_type": fu["pathway_position_type"],
                    "functional_unit_id": fu["functional_unit_id"],
                    "functional_unit_logic": fu["functional_unit_logic"],
                    "gene_id": gene,
                    "entry_id": fu["entry_id"],
                    "evidence": fu["evidence"],
                    "notes": fu["notes"]
                })
        return pd.DataFrame(rows)

    def build_cytoscape_nodes(self):
        nodes = {}
        for fu in self.functional_units:
            nodes[fu["pathway_id"]] = {
                "node_id": fu["pathway_id"],
                "node_type": "pathway",
                "label": fu["pathway_id"],
                "extra": ""
            }
            nodes[fu["functional_unit_id"]] = {
                "node_id": fu["functional_unit_id"],
                "node_type": "functional_unit",
                "label": fu["functional_unit_id"],
                "extra": f"logic={fu['functional_unit_logic']}"
            }
            for g in fu["genes"]:
                nodes[g] = {
                    "node_id": g,
                    "node_type": "gene",
                    "label": g,
                    "extra": ""
                }
        return pd.DataFrame(nodes.values())

    def build_cytoscape_edges(self):
        edges = []
        for fu in self.functional_units:
            for g in fu["genes"]:
                edges.append({
                    "source": g,
                    "target": fu["functional_unit_id"],
                    "edge_type": "gene_to_FU",
                    "logic": fu["functional_unit_logic"],
                    "pathway_position_id": "",
                    "pathway_position_type": ""
                })
            edges.append({
                "source": fu["functional_unit_id"],
                "target": fu["pathway_id"],
                "edge_type": "FU_to_pathway",
                "logic": "",
                "pathway_position_id": fu["pathway_position_id"],
                "pathway_position_type": fu["pathway_position_type"]
            })
        return pd.DataFrame(edges)

    def write_flat_csv(self, path):
        df = self.to_flat_dataframe()
        df.to_csv(path, index=False)
        return df

    def write_cytoscape_csvs(self, node_path, edge_path):
        n = self.build_cytoscape_nodes()
        e = self.build_cytoscape_edges()
        n.to_csv(node_path, index=False)
        e.to_csv(edge_path, index=False)
        return n, e
