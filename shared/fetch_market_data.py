"""
Fetch historical OHLCV market data and store in PostgreSQL.

Usage:
    uv run python shared/fetch_market_data.py SPY 2010-01-01

This script is idempotent: re-running it for the same ticker/date range
will not create duplicate rows (handled via PostgreSQL UPSERT).
"""

import os
import sys
from datetime import date, datetime

import pandas as pd
import yfinance as yf
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Open a connection to the local PostgreSQL database."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def fetch_ohlcv(ticker: str, start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """
    Fetch daily OHLCV data from yfinance.

    Returns a DataFrame with columns:
        date, open, high, low, close, adjusted_close, volume
    """
    print(f"Fetching {ticker} from yfinance ({start_date} to {end_date or 'today'})...")

    # auto_adjust=False keeps both raw close and adjusted close separate
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    # yfinance returns a multi-index column (e.g. ('Close', 'SPY'))
    # We flatten it to a single level.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Standardize column names to match our schema
    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adjusted_close",
            "Volume": "volume",
        }
    )

    df = df.reset_index()
    df = df.rename(columns={"Date": "date"})
    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df[["date", "open", "high", "low", "close", "adjusted_close", "volume"]]


def store_ohlcv(ticker: str, df: pd.DataFrame, source: str = "yfinance") -> int:
    """
    Store OHLCV data into PostgreSQL using UPSERT semantics.

    If a row for (ticker, date) already exists, it is updated with the
    new values rather than duplicated.

    Returns the number of rows affected.
    """
    rows = [
        (
            ticker,
            row["date"],
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["adjusted_close"],
            row["volume"],
            source,
        )
        for _, row in df.iterrows()
    ]

    sql = """
        INSERT INTO market_data
            (ticker, date, open, high, low, close, adjusted_close, volume, source)
        VALUES %s
        ON CONFLICT (ticker, date) DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            adjusted_close = EXCLUDED.adjusted_close,
            volume = EXCLUDED.volume,
            source = EXCLUDED.source,
            fetched_at = now()
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, rows)
            conn.commit()
            return cursor.rowcount


def main():
    if len(sys.argv) < 3:
        print("Usage: python fetch_market_data.py <TICKER> <START_DATE> [END_DATE]")
        print("Example: python fetch_market_data.py SPY 2010-01-01")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    start_date = sys.argv[2]
    end_date = sys.argv[3] if len(sys.argv) > 3 else None

    df = fetch_ohlcv(ticker, start_date, end_date)
    print(f"Fetched {len(df)} rows for {ticker}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

    rows_affected = store_ohlcv(ticker, df)
    print(f"✅ Stored {rows_affected} rows in market_data")


if __name__ == "__main__":
    main()