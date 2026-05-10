# Verdict: Source 01 — VIX

**Source:** CBOE Volatility Index (VIX), via yfinance (`^VIX`)
**Target:** SPY Garman-Klass annualized volatility, t+1
**Evaluation date:** 2026-05-10
**Protocol version:** 0.1
**Layers applied:** 1, 2 (per graduated rigor schedule for Source #1)

---

## 1. Source Description

The CBOE Volatility Index (VIX) is a real-time measure of the market's
expectation of 30-day forward volatility on the S&P 500, computed from
prices of SPX options. Often called "the fear gauge," VIX is itself a
forward-looking, market-derived estimate of the same quantity this lab
is attempting to predict (SPY realized volatility).

VIX serves here primarily as a **calibration test** for the evaluation
pipeline rather than a discovery candidate.

## 2. Data Acquisition

- **Source:** yfinance, ticker `^VIX`
- **Period:** 2010-01-04 to 2026-05-08
- **Storage:** stored in `market_data` table under ticker `^VIX`
- **Preprocessing:** none beyond the standard OHLCV ingestion

## 3. Sample Period and Observations

- **Total joined observations** (VIX + SPY GK vol): 4,111 (after t+1
  alignment dropped the final row)
- **Training period:** 2010-01-04 to 2022-12-30 — 3,272 rows
- **Test period (out-of-sample):** 2024-01-02 to 2026-05-07 — 589 rows

## 4. Layer-by-Layer Results

### Layer 1: Statistical Association

| Test | Statistic | p-value | Result |
|---|---|---|---|
| Pearson correlation | r = 0.7167 | < 1e-300 | ✅ |
| Spearman rank correlation | ρ = 0.6762 | < 1e-300 | ✅ |
| Granger causality, lag 1 | F = 679.0 | 1.16e-138 | ✅ |
| Granger causality, lag 5 | F = 50.8 | 3.03e-51 | ✅ |
| Granger causality, lag 10 | F = 25.6 | 8.86e-48 | ✅ |

All tests pass the protocol threshold (p < 0.05) decisively.
Sample size 4,111 ≫ minimum threshold of 250.

### Layer 2: Out-of-Sample Predictive Value

| Model | Out-of-sample R² | RMSE |
|---|---|---|
| Linear regression on VIX[t] | 0.4584 | 5.064 |
| Naive baseline (vol[t]) | 0.3095 | 5.718 |
| **R² improvement** | **+0.1489** | — |

Protocol threshold: VIX must beat naive baseline by ≥ 0.02 in R²,
with Diebold-Mariano p < 0.10.

- ΔR² = 0.149 ≫ 0.02 ✅
- Diebold-Mariano statistic = 2.92, p = 3.48e-03 ✅

Both Layer 2 conditions are met.

## 5. Final Verdict

**Robust predictive signal at the layers tested.**

VIX strongly predicts next-day SPY realized volatility, with a large
and statistically significant out-of-sample improvement over the
random-walk baseline.

This result is unsurprising: VIX is constructed precisely to be a
forward-looking volatility measure. The value of this evaluation is
methodological — it confirms the evaluation pipeline correctly detects
a strong, well-known signal. Pipeline calibration is successful.

## 6. Limitations and Caveats

- **Layer 3 (economic significance) and Layer 4 (robustness) were not
  applied** at this stage per the graduated rigor schedule. A follow-up
  evaluation could test whether VIX-based forecasts translate into
  profitable volatility-trading strategies after costs.
- **VIX is not freely tradable**; this evaluation does not address how
  to implement the signal practically.
- **The relationship is highly persistent over time** but may shift
  during structural breaks (e.g. the 2020 COVID crash, the 2008-style
  liquidity events not included in the sample). Layer 4 robustness
  testing would be needed to characterize this.
- **The model used is intentionally simple** (univariate linear
  regression). More sophisticated models (GARCH, HAR-RV, ML-based)
  almost certainly extract more signal but were not tested here, as
  the goal was pipeline validation, not optimal forecasting.

## 7. Recommendation

VIX is a known strong baseline. Its primary use in this lab is as a
**reference benchmark** for evaluating other sources: any candidate
alternative data source should be assessed not only on whether it
predicts SPY volatility (which is easy if you simply replicate VIX),
but on whether it adds **incremental** information beyond VIX.

Future source evaluations (e.g. Polymarket, Kalshi, news sentiment)
should report performance both standalone and conditional on VIX
already being in the model.