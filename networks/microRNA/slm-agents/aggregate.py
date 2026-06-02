import pandas as pd
import sys

def aggregate_csv(input_file, output_file):
    # Read the CSV
    df = pd.read_csv(input_file)

    # Group by col1 and aggregate col2 values into space-separated strings
    df_agg = (
        df.groupby('col1')['col2']
        .apply(lambda x: ' '.join(x.astype(str)))
        .reset_index()
    )

    # Rename column
    df_agg.columns = ['col1', 'col2_agg']

    # Save to CSV
    df_agg.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.csv output.csv")
    else:
        aggregate_csv(sys.argv[1], sys.argv[2])
