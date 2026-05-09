# Volatility Estimator Calibration: Garman-Klass vs Close-to-Close

**Date:** 2026-05-09
**Context:** Initial verification of the SPY volatility target variable
defined in `framework/evaluation_protocol.md`.

## Question

After computing Garman-Klass (GK) annualized volatility on SPY (2010–present),
the mean was **10.87%**, which seemed lower than the textbook "SPY vol is
15-18%" intuition. Was the calculation wrong?

## Diagnostic

Compared GK against the standard close-to-close (CC) realized volatility,
21-day rolling window, annualized.

| Metric | Mean | Median |
|---|---|---|
| Garman-Klass (single-day) | 10.87% | 8.78% |
| Close-to-close (21-day rolling) | 14.76% | 12.57% |
| Ratio GK/CC | 0.74 | 0.70 |

## Conclusion

The Garman-Klass estimator naturally produces lower volatility values than
close-to-close because GK ignores overnight returns. The theoretical ratio
GK/CC is approximately 0.6–0.8; observed 0.74 is consistent with this.

**Verdict: GK calculation is correct.** The original "15-18%" intuition
referred to close-to-close volatility, not GK. Both estimators are valid;
GK is more efficient (lower variance) but does not capture overnight gaps.

## Implication for the Protocol

The Evaluation Protocol uses GK as the primary target variable. This is
defensible because:

1. GK has lower estimator variance, making subtle predictive signals
   easier to detect.
2. Daily GK can be computed from a single trading day's OHLC, no rolling
   window needed.
3. The lower absolute value does not affect predictive analysis, since
   we evaluate sources on their ability to forecast *relative* volatility,
   not absolute levels.

For interpretability in human-readable reports, both GK and CC values
should be reported side by side.

## Open question (revisit later)

Should the protocol also include close-to-close as a secondary target,
to enable cross-validation of source signals against both estimators?
This would be a small extension at v0.2 or later.