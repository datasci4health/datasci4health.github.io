from lxml import etree
import pandas as pd
from collections import defaultdict
import uuid


class KeggKgmlToNetwork:
    """
    Parse KEGG KGML files and extract:
      - Gene → Functional Unit (FU)
      - FU → Pathway relationships
    with explicit AND / OR logic.

    Can export:
      - Flat gene–FU–pathway CSV
      - Cytoscape-compatible node and edge CSVs
    """

    def __init__(self, kgml_path):
        self.kgml_path = kgml_path
        self.root = None
        self.functional_units = []

    # ------------------------------------------------------------------
    # KGML parsing
    # ------------------------------------------------------------------

    def parse_kgml(self):
        tree = etree.parse(self.kgml_path)
        self.root = tree.getroot()
        return self.root

    @staticmethod
    def _parse_gene_names(name_field):
        if not name_field:
            return []
        return name_field.strip().split()

    # ------------------------------------------------------------------
    # Functional Unit extraction
    # ------------------------------------------------------------------

    def extract_functional_units(self):
        if self.root is None:
            self.parse_kgml()

        entries = {}
        groups = {}

        pathway_id = self.root.attrib.get("name", "unknown_pathway")

        # --- Collect entries ---
        for entry in self.root.findall("entry"):
            entry_id = entry.attrib["id"]
            entries[entry_id] = {
                "entry_id": entry_id,
                "type": entry.attrib.get("type"),
                "name": entry.attrib.get("name"),
                "reaction": entry.attrib.get("reaction", "").split(),
                "components": []
            }

        # --- Collect groups (complexes) ---
        for entry in self.root.findall("entry"):
            if entry.attrib.get("type") == "group":
                group_id = entry.attrib["id"]
                groups[group_id] = [
                    c.attrib["id"] for c in entry.findall("component")
                ]

        functional_units = []

        # --- Group entries → AND logic ---
        for group_id, component_ids in groups.items():
            genes = []
            reactions = set()

            for cid in component_ids:
                comp = entries.get(cid)
                if comp and comp["type"] == "gene":
                    genes.extend(self._parse_gene_names(comp["name"]))
                    reactions.update(comp["reaction"])

            fu_id = f"FU_{uuid.uuid4().hex[:8]}"

            for target in reactions or [group_id]:
                functional_units.append({
                    "pathway_id": pathway_id,
                    "pathway_position_id": target,
                    "pathway_position_type": (
                        "reaction" if target.startswith("rn:") else "node"
                    ),
                    "functional_unit_id": fu_id,
                    "functional_unit_logic": "AND",
                    "genes": genes,
                    "entry_id": group_id,
                    "evidence": "KGML",
                    "notes": "protein complex inferred from group"
                })

        # --- Gene entries → SINGLE or OR logic ---
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
                functional_units.append({
                    "pathway_id": pathway_id,
                    "pathway_position_id": target,
                    "pathway_position_type": (
                        "reaction" if target.startswith("rn:") else "node"
                    ),
                    "functional_unit_id": fu_id,
                    "functional_unit_logic": logic,
                    "genes": genes,
                    "entry_id": entry["entry_id"],
                    "evidence": "KGML",
                    "notes": "isozyme group" if logic == "OR" else ""
                })

        self.functional_units = functional_units
        return functional_units

    # ------------------------------------------------------------------
    # Flat CSV export (gene–FU–pathway)
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

    # ------------------------------------------------------------------
    # Cytoscape export
    # ------------------------------------------------------------------

    def build_cytoscape_nodes(self):
        nodes = {}

        for fu in self.functional_units:
            # Pathway node
            pid = fu["pathway_id"]
            nodes[pid] = {
                "node_id": pid,
                "node_type": "pathway",
                "label": pid,
                "extra": ""
            }

            # Functional Unit node
            fu_id = fu["functional_unit_id"]
            nodes[fu_id] = {
                "node_id": fu_id,
                "node_type": "functional_unit",
                "label": fu_id,
                "extra": f"logic={fu['functional_unit_logic']}"
            }

            # Gene nodes
            for gene in fu["genes"]:
                nodes[gene] = {
                    "node_id": gene,
                    "node_type": "gene",
                    "label": gene,
                    "extra": ""
                }

        return pd.DataFrame(nodes.values())

    def build_cytoscape_edges(self):
        edges = []

        for fu in self.functional_units:
            fu_id = fu["functional_unit_id"]
            pathway_id = fu["pathway_id"]

            # Gene → FU edges
            for gene in fu["genes"]:
                edges.append({
                    "source": gene,
                    "target": fu_id,
                    "edge_type": "gene_to_FU",
                    "logic": fu["functional_unit_logic"],
                    "pathway_position_id": "",
                    "pathway_position_type": ""
                })

            # FU → Pathway edge
            edges.append({
                "source": fu_id,
                "target": pathway_id,
                "edge_type": "FU_to_pathway",
                "logic": "",
                "pathway_position_id": fu["pathway_position_id"],
                "pathway_position_type": fu["pathway_position_type"]
            })

        return pd.DataFrame(edges)

    # ------------------------------------------------------------------
    # CSV writers
    # ------------------------------------------------------------------

    def write_flat_csv(self, filepath):
        df = self.to_flat_dataframe()
        df.to_csv(filepath, index=False)
        return df

    def write_cytoscape_csvs(self, node_path, edge_path):
        nodes_df = self.build_cytoscape_nodes()
        edges_df = self.build_cytoscape_edges()

        nodes_df.to_csv(node_path, index=False)
        edges_df.to_csv(edge_path, index=False)

        return nodes_df, edges_df
