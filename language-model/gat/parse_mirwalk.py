"""
parse_mirwalk.py
────────────────
Converts a miRWalk output file (with a `duplex` column) into the
mir_sequence.csv format expected by gat_pipeline.py.

miRWalk duplex field format:
    <miRNA_seq>#<mRNA_binding_site>#<dot-bracket_structure>

This script extracts the miRNA sequence (first field), converts T→U,
deduplicates by miRNA id, and writes mir_sequence.csv.

Usage:
    python parse_mirwalk.py \
        --input  mirwalk_output.csv \
        --output mir_sequence.csv \
        [--mir-col   mirna_id]   \
        [--duplex-col duplex]    \
        [--dna]                  # keep T instead of converting to U
"""

import argparse
import sys
import pandas as pd
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(
        description="Extract miRNA sequences from miRWalk duplex column",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--input",       required=True, help="miRWalk output CSV/TSV")
    p.add_argument("--output",      default="mir_sequence.csv",
                   help="Output path for mir_sequence.csv")
    p.add_argument("--mir-col",     default="mirna_id",
                   help="Column name that holds the miRNA identifier")
    p.add_argument("--duplex-col",  default="duplex",
                   help="Column name that holds the duplex string")
    p.add_argument("--dna",         action="store_true",
                   help="Keep T (DNA alphabet) instead of converting to U (RNA)")
    p.add_argument("--sep",         default=",",
                   help="Delimiter used in the input file (, or \\t)")
    return p.parse_args()


def extract_mirna_sequence(duplex: str, to_rna: bool = True) -> str:
    """
    Parse a miRWalk duplex string and return the mature miRNA sequence.

    Format:  <miRNA>#<mRNA_site>#<dot-bracket>
    The miRNA sequence is the first '#'-delimited field.
    T is converted to U unless to_rna=False.
    """
    if not isinstance(duplex, str) or not duplex.strip():
        return ""
    parts = duplex.split("#")
    if not parts:
        return ""
    seq = parts[0].strip().upper()
    if to_rna:
        seq = seq.replace("T", "U")
    return seq


def extract_mrna_site(duplex: str) -> str:
    """Return the mRNA target binding site (second field)."""
    if not isinstance(duplex, str):
        return ""
    parts = duplex.split("#")
    return parts[1].strip().upper() if len(parts) > 1 else ""


def extract_structure(duplex: str) -> str:
    """Return the dot-bracket secondary structure string (third field)."""
    if not isinstance(duplex, str):
        return ""
    parts = duplex.split("#")
    return parts[2].strip() if len(parts) > 2 else ""


def main():
    args = parse_args()
    sep = "\t" if args.sep in ("\\t", "\t", "tab") else args.sep

    # ── Load ────────────────────────────────────────────────────────────
    print(f"Reading: {args.input}")
    try:
        df = pd.read_csv(args.input, sep=sep, dtype=str)
    except Exception as e:
        sys.exit(f"Could not read input file: {e}")

    df.columns = df.columns.str.strip().str.lower()
    mir_col    = args.mir_col.lower()
    duplex_col = args.duplex_col.lower()

    if mir_col not in df.columns:
        print(f"  [warn] Column '{mir_col}' not found.")
        print(f"  Available columns: {list(df.columns)}")
        print("  Use --mir-col to specify the correct column name.")
        # try to auto-detect
        candidates = [c for c in df.columns if "mir" in c and "id" in c]
        if candidates:
            mir_col = candidates[0]
            print(f"  Auto-detected miRNA id column: '{mir_col}'")
        else:
            sys.exit("Cannot find miRNA id column. Aborting.")

    if duplex_col not in df.columns:
        print(f"  [warn] Column '{duplex_col}' not found.")
        print(f"  Available columns: {list(df.columns)}")
        candidates = [c for c in df.columns if "duplex" in c or "seq" in c]
        if candidates:
            duplex_col = candidates[0]
            print(f"  Auto-detected duplex column: '{duplex_col}'")
        else:
            sys.exit("Cannot find duplex column. Aborting.")

    print(f"  Rows loaded:   {len(df)}")
    print(f"  miRNA id col:  '{mir_col}'")
    print(f"  duplex col:    '{duplex_col}'")

    # ── Extract ─────────────────────────────────────────────────────────
    to_rna = not args.dna
    df["_mir_seq"]  = df[duplex_col].apply(lambda x: extract_mirna_sequence(x, to_rna))
    df["_mrna_site"]= df[duplex_col].apply(extract_mrna_site)
    df["_structure"] = df[duplex_col].apply(extract_structure)

    # Report parsing stats
    empty = (df["_mir_seq"] == "").sum()
    if empty:
        print(f"  [warn] {empty} rows had empty or unparseable duplex values.")

    # Deduplicate: one sequence per unique miRNA id
    # If the same miR appears multiple times (targeting different genes),
    # all copies share the same mature miRNA sequence — keep first.
    before = len(df)
    out = (
        df[[mir_col, "_mir_seq"]]
        .rename(columns={mir_col: "id", "_mir_seq": "sequence"})
        .query("sequence != ''")
        .drop_duplicates(subset="id")
        .reset_index(drop=True)
    )
    print(f"  Unique miRNAs after deduplication: {len(out)}  (from {before} rows)")

    # ── Validate sequences ───────────────────────────────────────────────
    valid_chars = set("ACGU" if to_rna else "ACGT")
    def is_valid(seq):
        return all(c in valid_chars for c in seq.upper())

    invalid = out[~out["sequence"].apply(is_valid)]
    if not invalid.empty:
        print(f"  [warn] {len(invalid)} sequences contain unexpected characters:")
        for _, row in invalid.head(5).iterrows():
            print(f"    {row['id']}: {row['sequence'][:40]}")

    # ── Write ────────────────────────────────────────────────────────────
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print(f"\n✓ Wrote {len(out)} miRNA sequences → {out_path}")

    # ── Also report what was NOT used ────────────────────────────────────
    extras = df[[mir_col, "_mrna_site", "_structure"]].copy()
    extras = extras.rename(columns={mir_col: "id", "_mrna_site": "mrna_site", "_structure": "dot_bracket"})
    side_path = out_path.parent / (out_path.stem + "_full_duplex.csv")
    df[[mir_col, duplex_col, "_mir_seq", "_mrna_site", "_structure"]].to_csv(side_path, index=False)
    print(f"  Full duplex table (with mRNA site + structure) → {side_path}")
    print("\nNote: the mRNA binding sites and dot-bracket structures are preserved")
    print("in the _full_duplex.csv for future use (e.g. structure-aware encoders).")


if __name__ == "__main__":
    main()
