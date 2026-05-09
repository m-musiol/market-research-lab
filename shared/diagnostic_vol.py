"""
Diagnostic: compare Garman-Klass vs simple close-to-close realized vol.
This helps verify the GK calculation is in the right ballpark.
"""
import os
import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

# Load SPY data
df = pd.read_sql(
    "SELECT date, open, high, low, close FROM market_data WHERE ticker='SPY' ORDER BY date",
    conn,
)
conn.close()

# Method 1: Garman-Klass (what we computed)
log_hl = np.log(df["high"] / df["low"])
log_co = np.log(df["close"] / df["open"])
gk_daily_var = 0.5 * log_hl**2 - (2 * np.log(2) - 1) * log_co**2
gk_annualized_pct = np.sqrt(gk_daily_var * 252) * 100

# Method 2: Close-to-close (the standard benchmark)
log_returns = np.log(df["close"] / df["close"].shift(1))
# Rolling 21-day std, annualized
cc_rolling_pct = log_returns.rolling(21).std() * np.sqrt(252) * 100

print("=" * 60)
print("VOLATILITY COMPARISON: SPY (2010-present)")
print("=" * 60)
print(f"\nGarman-Klass (single-day estimator):")
print(f"  Mean:   {gk_annualized_pct.mean():.2f}%")
print(f"  Median: {gk_annualized_pct.median():.2f}%")

print(f"\nClose-to-close (21-day rolling, standard benchmark):")
print(f"  Mean:   {cc_rolling_pct.mean():.2f}%")
print(f"  Median: {cc_rolling_pct.median():.2f}%")

print(f"\nRatio GK/CC: {gk_annualized_pct.mean() / cc_rolling_pct.mean():.2f}")
print("(Theoretical: ~0.6-0.8 because GK ignores overnight gaps)")