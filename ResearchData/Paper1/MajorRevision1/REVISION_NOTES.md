# Revision notes — Major Revision 1

Point-by-point record of what changed in response to the co-author's memo on the first draft
(`../manuscript/paper1_reciprocity_regime.md`). Every change is reproducible from
`bash run_all.sh`; the parent paper is untouched.

## The memo, and the response

| Memo point | Response | Where |
|---|---|---|
| Write towards three to five statistics. | The paper is re-organised around exactly the five the memo named: (1) same-day r with a zero-lag VAR and no Granger causality; (2) the regime contrast 0.69 / 0.18 / 0.66, Fisher z p = 0.0007; (3) the FEVD reversal 41/2 vs 44/0.2; (4) the ratio flip 0.68 → 1.42 with 13 countries by Day 22 and none after; (5) diplomacy, weekly r = 0.06 against regime-level movement. Each has its own results subsection, table, and figure. | §4.1–4.5, Tables 2–6, Figures 2–6 |
| Give the FEVD under-identification result more prominence; it is the methodological contribution and protects the paper from "who started it". | Promoted from a sub-point to Finding 3 with its own table and figure; the mechanism (ρ² = 0.38 of same-day variance handed to whichever series is ordered first) is stated in plain terms; the abstract and the discussion bullets carry it. | §4.3, Table 4, Figure 4 |
| The resumption-phase Granger result rests on 23 daily observations: report as suggestive. | Re-reported with the number of usable observations (22), under two operationalisations (null under raw rows, p = 0.78), and labelled suggestive in the results, the discussion, and the co-author brief. | §4.7, Table 8 |
| Keep the full-sample p-value out of the abstract, or re-estimate on a regime-demeaned series. | Both. The abstract carries no full-sample p-value. The full-sample VAR is re-estimated with the four phase means removed (and, as a sensitivity, the six detected regime means); BIC selects lag 0 on the demeaned series; the retal→strikes test ranges from p = 0.0009 to 0.26 across specifications; strikes→retal is never significant. | §4.7, Table 8, `08_directional_scoping.py` |
| "Retaliation Granger-causes strikes" → compellence is doing too much work; tit-for-tat and threshold-triggered punishment are equally consistent. Abstract "compellence-consistent" is fine; discussion "reactive (compellence)" reads as confirmed. | The word "reactive" is gone. The abstract makes no compellence claim; the discussion bullet names tit-for-tat and threshold-triggered punishment as equally consistent and fixes "compellence-consistent" as the strongest defensible phrase. | Abstract; §6 bullet 4 |
| The depletion reading needs its alternatives named: deliberate restraint, proxy rather than direct action, shifts in reporting attention. | Named in the discussion bullet and in the co-author brief; the results section for Finding 4 defers interpretation to the discussion. | §4.4, §6 bullet 5 |
| Add a placebo or permutation check on the break dates ("is six regimes BIC finding structure or finding noise?"). | Added. Three nulls × 1,000 seeded draws (shuffled days; AR(1) with within-regime persistence 0.29; AR(1) with whole-series persistence 0.71). Result: the segment count is not evidence (BIC over-selects on noise), but the observed fit improvement (170.3 BIC points) exceeds every one of the 3,000 draws (p = 0.001 against each). Plus a sensitivity grid over stricter penalties (Yao BIC, LWZ) and minimum segment lengths, and replication on the retaliation and combined series. The July breaks survive BIC-type criteria but not LWZ; this is stated. | §4.6, Table 7, Figure 7, `07_breaks_placebo.py` |
| Theory, discussion, and conclusion to be rewritten by hand by the co-author; methods, results, and robustness stay. | Introduction and Discussion are drafted as bullet points (seven each, one per intended paragraph), with the literature left for the co-author to characterise. Methods, results, robustness, and limitations are complete. | §1, §6 |
| Bai–Perron recovers the narrative boundaries within 1, 1, 6 days without being told where to look — evidence in its own right. | Kept, stated with the gaps (−1, +1, −6) in Table 7's note and in the abstract. | §4.6 |
| The tests do not need changing for this audience. | No test was removed. VAR, Granger, IRF, FEVD, Bai–Perron, and negative binomial are all retained; each is introduced in one plain sentence before its specification. | §3 |

## Other changes

- **Impulse-response error band corrected.** The parent paper's Figure 3 used statsmodels'
  `errband_mc(seed=…)`, which passes the same seed to every Monte-Carlo replication and so
  collapses the band to a line. The revision draws a fresh seed per replication from one
  seeded generator (`mc_errband()` in `02_reciprocity_var.py`). The point estimates are
  unchanged (impact 2.28, cumulative 4.55); the corrected 95% band includes zero from the
  first day after the shock. This strengthens Finding 1.
- **Fisher comparisons completed.** The parent reported combat vs ceasefire only. The revision
  reports all three pairwise comparisons with Holm adjustment (ceasefire vs resumption
  p = 0.013; combat vs resumption p = 0.87).
- **Bootstrap intervals for the ratio.** The ratio flip is now reported with seeded bootstrap
  95% intervals (0.59–0.77 vs 0.94–2.32; non-overlapping).
- **Regime-level diplomacy test.** Kruskal–Wallis across phases (H = 55.0, p < 0.001,
  ε² = 0.33) quantifies the regime-level movement the memo describes; the weekly rank
  correlation (0.36, p = 0.08) is reported alongside the Pearson r = 0.06.
- **Casualty series removed from the main figures.** Deaths appear only in the robustness
  caveat (tempo is not a lethality proxy), as in the parent.
- **Format.** Broadly APA 7 Word manuscript (title page, abstract, numbered tables with notes,
  figures with captions, hanging-indent references, appendix), built from the markdown source
  with every table injected from the regenerated CSVs and cross-checked against the markdown.
- **Integrity.** The input's MD5 is verified; the panel is asserted identical to the parent's;
  the synthesis step asserts every headline number and checks that each appears verbatim in
  the manuscript.

## Numbers that changed relative to the parent draft

None of the parent's point estimates changed. What changed is scope and presentation: the
full-sample Granger p-value left the abstract; the resumption result is labelled suggestive;
the IRF band is now a real band; and the new placebo, sensitivity, bootstrap, Holm, and
Kruskal–Wallis numbers are additions.
