import pandas as pd
import os
from pathlib import Path

def concatenate_csvs(input_dir, output_file):
    all_files = list(Path(input_dir).glob("*.csv"))
    df_list = []

    for file in all_files:
        df = pd.read_csv(file)
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined {len(all_files)} files into {output_file}")

# Example usage
if __name__ == "__main__":
    concatenate_csvs("./", "combined_sanctions.csv")