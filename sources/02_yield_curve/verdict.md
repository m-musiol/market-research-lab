# Verdict: Source 02 — Treasury Yield Curve (10Y-2Y Spread)

**Source:** 10Y-2Y Treasury spread, computed from FRED series `DGS10` and `DGS2`
**Target:** SPY Garman-Klass annualized volatility, t+1
**Evaluation date:** 2026-05-13
**Protocol version:** 0.1
**Layers applied:** 1, 2 (per graduated rigor schedule for Source #2)

---

## 1. Source Description

The 10Y-2Y Treasury spread is the difference between the constant
maturity 10-year and 2-year US Treasury yields. A negative spread
("inverted yield curve") is one of the most-watched recession
predictors in macroeconomics, with a strong empirical track record
preceding US recessions over the past 50+ years.

This evaluation tests a different and narrower question: whether the
spread carries predictive information about *daily equity volatility*,
on a one-day-ahead horizon.

## 2. Data Acquisition

- **Sources:** FRED, series `DGS10` (10-Year Treasury Constant Maturity
  Rate) and `DGS2` (2-Year Treasury Constant Maturity Rate)
- **Derived signal:** `spread = DGS10 − DGS2`
- **Period:** 2010-01-04 to 2026-05-13
- **Storage:** `source_signals` table, `source_name = 'yield_curve'`,
  signals `dgs10`, `dgs2`, `spread_10y_2y`
- **Preprocessing:** FRED's missing-value markers (`.`) dropped before
  storage. Spread computed only on dates where both series available.

## 3. Sample Period and Observations

- **Total joined observations** (yield spread + SPY GK vol, after t+1
  alignment): 4,081
- **Training period:** 2010-01-04 to 2022-12-30 — 3,247 rows
- **Test period (out-of-sample):** 2024-01-02 to 2026-05-07 — 585 rows

Note: most of the training period featured a normal (positively sloped)
curve, while the test period sat predominantly within the deep
inversion of 2023-2024. This regime mismatch is consequential for the
Layer 2 result; see section 6.

## 4. Layer-by-Layer Results

### Layer 1: Statistical Association

| Test | Statistic | p-value | Result |
|---|---|---|---|
| Pearson correlation | r = -0.0413 | 8.25e-03 | "significant" but effect tiny |
| Spearman rank correlation | ρ = -0.0426 | 6.45e-03 | same |
| Granger causality, lag 1 | F = 1.29 | 2.56e-01 | not significant |
| Granger causality, lag 5 | F = 2.71 | 1.90e-02 | significant |
| Granger causality, lag 10 | F = 2.28 | 1.19e-02 | significant |

By the strict letter of protocol v0.1, Layer 1 passes — both
correlation p-values are below 0.05 and two of three Granger lags
reach significance.

By **effect size**, the relationship is negligible. Pearson r² ≈ 0.0017
means the spread explains roughly 0.17% of the variance in next-day
volatility. This is a textbook case of a large sample (n = 4,081)
making a near-zero correlation statistically significant.

The sign of the correlation is negative (flatter or inverted curve →
slightly higher next-day volatility), which is economically sensible —
yield curve stress and equity volatility plausibly share a common
driver in macro uncertainty. The Granger pattern (no signal at lag 1,
weak signal at lags 5-10) is also consistent with the slow-moving
nature of the yield curve as a macro variable.

### Layer 2: Out-of-Sample Predictive Value

| Model | Out-of-sample R² | RMSE |
|---|---|---|
| Linear regression on spread[t] | **-0.1037** | 7.249 |
| Naive baseline (vol[t]) | 0.3194 | 5.692 |
| **R² differential** | **-0.4231** | — |

Protocol threshold: spread must beat naive by ≥ 0.02 in R², with
Diebold-Mariano p < 0.10.

- ΔR² = -0.42 ❌ (model is dramatically worse than baseline)
- Diebold-Mariano statistic = 2.91, p = 3.61e-03 ❌
  (the spread model's errors are *significantly larger* than naive's)

**Layer 2 fails decisively.** The spread model is not merely no better
than the naive baseline — it is significantly worse.

## 5. Final Verdict

**Statistically detectable but practically negligible association
in-sample; actively harmful out-of-sample at the daily horizon.**

The yield curve spread does not predict next-day SPY realized
volatility. The marginal in-sample correlation is an artifact of
large sample size rather than a meaningful signal.

## 6. Limitations and Caveats

- **Regime mismatch in train vs. test.** The training period
  (2010-2022) was dominated by a normal, positively-sloped yield curve.
  The test period (2024-2026) sat largely within a deep inversion.
  Models trained on one regime can fail catastrophically when applied
  to another. This contributes to the magnitude of the Layer 2 failure
  but does not change the conclusion: even within the training period,
  the in-sample signal was negligible.

- **Wrong horizon.** The yield curve is a well-validated *recession*
  predictor at multi-quarter horizons, not a *daily volatility*
  predictor. The negative result reflects mismatch between source and
  target, not a flaw in the source itself. A longer-horizon evaluation
  (e.g. 1-month or 3-month forward volatility) could yield a different
  result and may be worth running as a separate study.

- **Linear model only.** A linear regression cannot capture potential
  non-linear effects, such as a "threshold effect" where the curve
  matters only when deeply inverted. This was not tested.

- **Protocol gap exposed.** This evaluation exposed a gap in protocol
  v0.1: Layer 1 uses only a p-value threshold and does not require a
  minimum effect size. With n > 4,000, near-zero correlations cross
  the p < 0.05 threshold. The protocol should be amended to v0.2 with
  an explicit effect-size requirement. See `notes/02_protocol_gap_*.md`
  (forthcoming) for the proposed amendment.

## 7. Recommendation

For the daily-horizon SPY volatility target defined in protocol v0.1,
the 10Y-2Y Treasury spread should **not** be used — neither as a
standalone signal nor as an additive feature alongside stronger
predictors like VIX. It contains effectively no information about
next-day volatility, and out-of-sample it actively degrades naive
forecasts.

The spread may still be informative for:
- **Longer-horizon volatility** (monthly or quarterly), worth a
  separate evaluation outside this protocol
- **Recession or macro-regime forecasting**, which is a different
  target outside this lab's current scope
- **Conditional or non-linear models** (e.g. a regime-switching
  framework where the spread acts as a regime indicator)

None of these alternatives is pursued here. For protocol v0.1, the
verdict stands.