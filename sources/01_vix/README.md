# Source 01: VIX (CBOE Volatility Index)

## Source Description

The CBOE Volatility Index (VIX) is a real-time measure of the market's
expectation of 30-day forward volatility on the S&P 500, derived from
prices of SPX options. It is widely known as "the fear gauge."

VIX is forward-looking by construction: it represents the implied
volatility priced into options, not realized historical volatility.

## Hypothesis

VIX, measured at the close of day t, contains predictive information
about realized volatility on day t+1.

This is treated as a **calibration test** for the evaluation pipeline.
A mature, deeply-studied source like VIX should pass Layer 1
(statistical association). If it does not, the evaluation pipeline
itself is suspect.

## Data Acquisition

- Source: yfinance, ticker `^VIX`
- Frequency: daily close
- Period: 2010-01-01 to present (matching SPY history)

## Evaluation Layers

Per the graduated rigor schedule (Source #1 → Layers 1-2):

- **Layer 1:** Statistical association between VIX[t] and SPY GK
  volatility[t+1]
- **Layer 2:** Out-of-sample predictive value vs. naive baseline

Layers 3 and 4 are skipped at this stage.

## Files

- `README.md` — this file
- `fetch.py` — data acquisition
- `analysis.ipynb` — notebook with statistical tests and visualizations
- `verdict.md` — final structured verdict