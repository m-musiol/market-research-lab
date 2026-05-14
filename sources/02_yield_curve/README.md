# Source 02: Treasury Yield Curve

## Source Description

The US Treasury yield curve describes the interest rates the US
government pays across different borrowing maturities. The most-watched
summary statistic is the 10Y-2Y spread: the difference between the
10-year and 2-year Treasury Constant Maturity rates.

A negative spread ("inverted curve") is a well-known recession
predictor. This evaluation tests whether the spread also carries
predictive information about short-term equity market volatility.

## Hypothesis

The 10Y-2Y Treasury spread, measured at the close of day t, contains
predictive information about SPY realized volatility on day t+1.

Unlike VIX (Source 01), this is an **indirect, cross-domain, slow-moving**
signal. It serves as a second calibration test: it confirms whether the
evaluation pipeline behaves sensibly on a signal type very different
from a direct volatility measure.

## Data Acquisition

- Source: FRED (Federal Reserve Economic Data)
- Series: `DGS10` (10-Year Treasury), `DGS2` (2-Year Treasury)
- Derived signal: `spread_10y_2y = DGS10 - DGS2`
- Frequency: daily
- Period: 2010-01-01 to present (matching SPY history)

## Evaluation Layers

Per the graduated rigor schedule (Source #2 -> Layers 1-2):

- **Layer 1:** Statistical association between the 10Y-2Y spread at
  day t and SPY GK volatility at day t+1
- **Layer 2:** Out-of-sample predictive value vs. naive baseline

Layers 3 and 4 are skipped at this stage.

## Note on Expectations

It is genuinely uncertain whether the yield curve spread predicts
*daily* volatility. It is a strong *recession* predictor, but daily
volatility is a noisier, shorter-horizon target. A Layer 1 failure
would be a valid and informative result, not a pipeline error.

## Files

- `README.md` — this file
- `fetch.py` — data acquisition from FRED
- `analysis.ipynb` — statistical tests and visualizations
- `verdict.md` — final structured verdict