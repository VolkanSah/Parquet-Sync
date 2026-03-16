import polars as pl
import os
import sys

def sync():
    # 1. RAW -> EDITABLE (Neue Originale verarbeiten)
    for f in os.listdir('raw'):
        if f.endswith('.parquet'):
            csv_name = f.replace('.parquet', '.csv')
            if not os.path.exists(f'editable/{csv_name}'):
                print(f"Generating editable copy for {f}")
                df = pl.read_parquet(f'raw/{f}')
                df.write_csv(f'editable/{csv_name}')

    # 2. EDITABLE -> EXPORTS (Geänderte CSVs zu Parquet machen)
    for f in os.listdir('editable'):
        if f.endswith('.csv'):
            parquet_name = f.replace('.csv', '.parquet')
            print(f"Syncing {f} to exports...")
            df = pl.read_csv(f'editable/{f}')
            df.write_parquet(f'exports/{parquet_name}')

if __name__ == "__main__":
    sync()
