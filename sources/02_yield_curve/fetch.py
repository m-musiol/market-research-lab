"""
Fetch Treasury yield data from FRED and store in source_signals.

Fetches:
  - DGS10: 10-Year Treasury Constant Maturity Rate
  - DGS2:  2-Year Treasury Constant Maturity Rate

Computes and stores three signals under source_name = 'yield_curve':
  - dgs10           (raw 10-year yield)
  - dgs2            (raw 2-year yield)
  - spread_10y_2y   (DGS10 - DGS2, the derived signal we evaluate)

Run from repo root:
    uv run python sources/02_yield_curve/fetch.py
"""

import os
from pathlib import Path

import pandas as pd
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Repo root (hardcoded; scripts may be launched from various working dirs)
REPO_ROOT = Path(r"C:\Users\marcm\datascience\DS\Projects\market-research-lab")
load_dotenv(REPO_ROOT / ".env")

SOURCE_NAME = "yield_curve"
START_DATE = "2010-01-01"


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def fetch_fred_series(series_id: str, start_date: str) -> pd.DataFrame:
    """
    Fetch a single FRED series via the FRED API.

    Returns a DataFrame with columns: date, value
    Missing observations (FRED marks them ".") are dropped.
    """
    api_key = os.getenv("FRED_API_KEY")
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
    }

    print(f"Fetching FRED series {series_id}...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    observations = response.json()["observations"]
    df = pd.DataFrame(observations)[["date", "value"]]

    # FRED marks missing values with "." — drop those rows
    df = df[df["value"] != "."].copy()
    df["value"] = df["value"].astype(float)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    print(f"  Retrieved {len(df)} observations "
          f"({df['date'].min()} to {df['date'].max()})")
    return df


def store_signal(source_name: str, signal_name: str, df: pd.DataFrame) -> None:
    """Store a signal series in source_signals via UPSERT."""
    rows = [
        (source_name, signal_name, row["date"], row["value"])
        for _, row in df.iterrows()
    ]

    sql = """
        INSERT INTO source_signals (source_name, signal_name, date, value)
        VALUES %s
        ON CONFLICT (source_name, signal_name, date) DO UPDATE SET
            value = EXCLUDED.value,
            fetched_at = now()
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, rows)
            conn.commit()

    print(f"  Stored signal '{signal_name}' ({len(rows)} rows)")


def main():
    # Fetch the two raw series
    dgs10 = fetch_fred_series("DGS10", START_DATE)
    dgs2 = fetch_fred_series("DGS2", START_DATE)

    # Store the raw series
    store_signal(SOURCE_NAME, "dgs10", dgs10)
    store_signal(SOURCE_NAME, "dgs2", dgs2)

    # Compute the spread — only on dates where BOTH series exist
    merged = dgs10.merge(dgs2, on="date", suffixes=("_10y", "_2y"))
    merged["spread"] = merged["value_10y"] - merged["value_2y"]
    spread_df = merged[["date", "spread"]].rename(columns={"spread": "value"})

    store_signal(SOURCE_NAME, "spread_10y_2y", spread_df)

    print()
    print(f"✅ Done. Spread series: {len(spread_df)} rows "
          f"({spread_df['date'].min()} to {spread_df['date'].max()})")
    print(f"   Spread range: {spread_df['value'].min():.2f} to "
          f"{spread_df['value'].max():.2f}")
    # A negative minimum confirms we captured at least one inversion period
    n_inverted = (spread_df["value"] < 0).sum()
    print(f"   Days with inverted curve (spread < 0): {n_inverted}")


if __name__ == "__main__":
    main()