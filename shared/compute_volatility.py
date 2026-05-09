"""
Compute Garman-Klass volatility from stored OHLCV data and write it to
the volatility_metrics table.

Garman-Klass formula (from the Evaluation Protocol):
    σ²_GK = 0.5 * (ln(High/Low))² − (2*ln(2)−1) * (ln(Close/Open))²

This produces a daily *variance* estimate. To express in annualized
percentage points (the protocol's reporting unit), we:
    1. Multiply daily variance by 252 (trading days per year)
    2. Take the square root → annualized standard deviation
    3. Multiply by 100 → percentage points

Usage:
    uv run python shared/compute_volatility.py SPY
"""

import os
import sys

import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

METRIC_NAME = "garman_klass_annualized_pct"
TRADING_DAYS_PER_YEAR = 252


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def load_ohlcv(ticker: str) -> pd.DataFrame:
    """Load all OHLCV data for a ticker from PostgreSQL."""
    sql = """
        SELECT date, open, high, low, close
        FROM market_data
        WHERE ticker = %s
        ORDER BY date ASC
    """
    with get_db_connection() as conn:
        df = pd.read_sql(sql, conn, params=(ticker,))

    if df.empty:
        raise ValueError(f"No OHLCV data found for {ticker}")

    return df


def compute_garman_klass(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Garman-Klass daily variance, then annualize and convert to
    percentage points.

    Returns a DataFrame with columns: date, value
    """
    # Filter rows where any OHLC value is missing or non-positive
    # (log of zero or negative is undefined)
    valid = (
        (df["open"] > 0)
        & (df["high"] > 0)
        & (df["low"] > 0)
        & (df["close"] > 0)
    )
    df = df.loc[valid].copy()

    log_hl = np.log(df["high"] / df["low"])
    log_co = np.log(df["close"] / df["open"])

    # Daily variance per Garman-Klass
    daily_variance = 0.5 * (log_hl ** 2) - (2 * np.log(2) - 1) * (log_co ** 2)

    # Annualize and convert to percentage points
    annualized_std = np.sqrt(daily_variance * TRADING_DAYS_PER_YEAR)
    annualized_pct = annualized_std * 100

    return pd.DataFrame({"date": df["date"].values, "value": annualized_pct.values})


def store_volatility(ticker: str, df: pd.DataFrame) -> int:
    """Store volatility values via UPSERT."""
    rows = [(ticker, row["date"], METRIC_NAME, row["value"]) for _, row in df.iterrows()]

    sql = """
        INSERT INTO volatility_metrics (ticker, date, metric_name, value)
        VALUES %s
        ON CONFLICT (ticker, date, metric_name) DO UPDATE SET
            value = EXCLUDED.value,
            computed_at = now()
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, rows)
            conn.commit()
            return cursor.rowcount


def main():
    if len(sys.argv) < 2:
        print("Usage: python compute_volatility.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    print(f"Loading OHLCV data for {ticker}...")
    ohlcv = load_ohlcv(ticker)
    print(f"Loaded {len(ohlcv)} rows ({ohlcv['date'].min()} to {ohlcv['date'].max()})")

    print("Computing Garman-Klass volatility...")
    vol = compute_garman_klass(ohlcv)
    print(f"Computed {len(vol)} volatility values")
    print(f"  Mean:   {vol['value'].mean():.2f}%")
    print(f"  Median: {vol['value'].median():.2f}%")
    print(f"  Min:    {vol['value'].min():.2f}%")
    print(f"  Max:    {vol['value'].max():.2f}%")

    rows_affected = store_volatility(ticker, vol)
    print(f"✅ Stored volatility values in volatility_metrics")


if __name__ == "__main__":
    main()