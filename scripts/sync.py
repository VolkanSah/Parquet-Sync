import polars as pl
import os
import sys


def raw_to_editable():
    """Convert raw Parquet files to editable CSV format."""
    os.makedirs('editable', exist_ok=True)
    for f in os.listdir('raw'):
        if f.endswith('.parquet'):
            print(f"Converting {f} to CSV...")
            df = pl.read_parquet(f'raw/{f}')
            # Cast nested types (List, Struct, Array) to string before CSV export
            df = df.with_columns([
                pl.col(s).cast(pl.Utf8)
                for s, dtype in zip(df.columns, df.dtypes)
                if dtype in (pl.List, pl.Struct, pl.Array)
            ])
            df.write_csv(f"editable/{f.replace('.parquet', '.csv')}")
            print(f"  → editable/{f.replace('.parquet', '.csv')}")


def editable_to_export():
    """Convert edited CSV files back to Parquet for HF upload."""
    os.makedirs('exports', exist_ok=True)
    for f in os.listdir('editable'):
        if f.endswith('.csv'):
            print(f"Exporting {f} to Parquet...")
            df = pl.read_csv(f'editable/{f}')
            df.write_parquet(f"exports/{f.replace('.csv', '.parquet')}")
            print(f"  → exports/{f.replace('.csv', '.parquet')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync.py [to_editable|to_export]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "to_editable":
        raw_to_editable()
    elif mode == "to_export":
        editable_to_export()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python sync.py [to_editable|to_export]")
        sys.exit(1)
