"""
Convert a FASTA file to a CSV file with two columns: id and sequence.

Each FASTA header line starts with ">". The text after ">" becomes the id.
All following sequence lines are concatenated until the next header.

Usage:
    python language-model/gat/fasta_to_csv.py \
        --input networks/microRNA/ensembl/mart_export.fasta \
        --output language-model/gat/mapk/nodes-mapk-gene-sequence.csv
"""

import argparse
import csv
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert multiline FASTA records to id,sequence CSV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input", required=True, help="Input FASTA file")
    parser.add_argument("--output", required=True, help="Output CSV file")
    return parser.parse_args()


def read_fasta(path):
    """Yield (id, sequence) tuples from a FASTA file."""
    current_id = None
    sequence_parts = []

    with open(path, "r", encoding="utf-8") as fasta_file:
        for line_number, raw_line in enumerate(fasta_file, start=1):
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if current_id is not None:
                    yield current_id, "".join(sequence_parts)

                current_id = line[1:].strip()
                if not current_id:
                    raise ValueError(f"Empty FASTA id at line {line_number}")
                sequence_parts = []
            else:
                if current_id is None:
                    raise ValueError(
                        f"Sequence line found before first FASTA header at line {line_number}"
                    )
                sequence_parts.append(line)

    if current_id is not None:
        yield current_id, "".join(sequence_parts)


def write_csv(records, path):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "sequence"])
        writer.writerows(records)


def main():
    args = parse_args()
    records = list(read_fasta(args.input))
    write_csv(records, args.output)
    print(f"Wrote {len(records)} sequences to {args.output}")


if __name__ == "__main__":
    main()
