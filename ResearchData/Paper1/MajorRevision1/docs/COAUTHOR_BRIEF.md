# Co-author brief — the five statistics, where they live, and how far each claim goes

*For the co-author writing the Introduction, Discussion, and Conclusion by hand. Everything
here regenerates from `bash run_all.sh`; nothing in the manuscript exists that the pipeline
does not produce.*

## The five statistics to write towards

| # | Statistic | Value | Table / Figure | Script | Claim it licenses |
|---|---|---|---|---|---|
| 1 | Same-day r in combat, with a zero-lag VAR under every criterion and no Granger causality either way | r = 0.69 (0.48–0.82); lags 0/0/0/0; p = 0.78 and 0.44 | Table 2, Figure 2, Figure A1 | `02` | The exchange runs faster than the day. |
| 2 | Regime contrast | r = 0.69 / 0.18 / 0.66; Fisher z p = 0.0007 (Holm 0.002) | Table 3, Figure 3 | `03` | Reciprocity is switched on and off with the political regime. |
| 3 | FEVD reversal | 41% vs 2% under one ordering; 44% vs 0.2% under the other; ρ² = 0.38 | Table 4, Figure 4 | `04` | "Who set the tempo" is not identified at daily resolution (methodological contribution). |
| 4 | Ratio flip and reach | 0.68 (0.59–0.77) → 1.42 (0.94–2.32); 13 countries by Day 22, none after | Table 5, Figure 5 | `05` | Consistent with depletion **and** with three named alternatives. |
| 5 | Diplomacy | weekly r = 0.06 (n.s.); 3.2 → 0.4 events/day ceasefire → resumption; Kruskal–Wallis p < 0.001 | Table 6, Figure 6 | `06` | Diplomacy moved with the regime, not the week. |

Supporting results: regimes recovered within 1, 1, 6 days and the placebo (Table 7,
Figure 7, `07`); directional evidence scoped (Table 8, `08`); robustness (Table 9, `09`).

## Scoping language (what the numbers support)

- **Resumption direction (retaliation → strikes).** p = 0.026 on 22 usable observations under
  the primary measure; p = 0.78 under raw rows. Write "suggestive". Do not write "confirmed".
- **Full-sample direction.** After removing regime means, p = 0.055 at lag 1 and p = 0.0013 at
  the AIC lag; with the six detected regimes removed, p = 0.26 and p = 0.0009. Direction
  consistent, strength specification-dependent. Keep it out of the abstract (it is).
- **Compellence.** "Compellence-consistent" is defensible. The same pattern is also consistent
  with tit-for-tat and with punishment triggered by a threshold; say so.
- **Depletion.** Name the alternatives in place: deliberate restraint to keep the resumption
  limited; proxy rather than direct Iranian action; shifts in reporting attention.
- **Six regimes.** Do not lean on the count. The BIC picks six segments on persistent noise
  most of the time. Lean on the size of the improvement (170 vs placebo maxima 40/40/157,
  p = 0.001) and on the recovery of the documented dates. Note that the July breaks are found
  by BIC-type criteria but not by the strictest one (LWZ).

## Where each number comes from

```
output/tables/t02_same_day.csv         same-day r and CI
output/tables/t02_lag_selection.csv    AIC/BIC/HQIC/FPE lag choices
output/tables/t02_granger.csv          Granger tests (combat; naive full)
output/tables/t03_regime_coupling.csv  r by phase
output/tables/t03_fisher_pairwise.csv  Fisher z, Holm
output/tables/t04_fevd_orderings.csv   FEVD both orderings
output/tables/t05_ratio_by_phase.csv   ratio + bootstrap CI + lead-lag
output/tables/t05_spread.csv           13 countries by Day 22
output/tables/t06_*.csv                diplomacy
output/tables/t07_*.csv                breaks, placebo, sensitivity
output/tables/t08_*.csv                directional evidence, scoped
output/tables/t09_*.csv                robustness
output/synthesis.json                  all headline numbers, machine-readable
```

## What was changed in response to the memo

See `REVISION_NOTES.md` for the point-by-point list.
