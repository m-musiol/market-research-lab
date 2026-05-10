"""
Fetch VIX historical data and store in market_data table.

Run from repo root:
    uv run python sources/01_vix/fetch.py
"""

import sys
from pathlib import Path

# Add the repo root to Python path so we can import shared utilities
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.fetch_market_data import fetch_ohlcv, store_ohlcv


def main():
    ticker = "^VIX"
    start_date = "2010-01-01"

    print(f"Fetching {ticker}...")
    df = fetch_ohlcv(ticker, start_date)
    print(f"Fetched {len(df)} rows ({df['date'].min()} to {df['date'].max()})")

    rows = store_ohlcv(ticker, df, source="yfinance")
    print(f"✅ Stored VIX data ({rows} rows updated/inserted)")


if __name__ == "__main__":
    main()