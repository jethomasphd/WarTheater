# Baseline JSON Corrections — February 27, 2026

## Task

Update the pre-war baseline JSON object with the corrected values below. Each correction includes the verified value, the source, and the confidence level. Do not modify any field not listed here.

---

## Corrections

### oil.brent
- **Old:** `72.38`
- **New:** `71.00`
- **Source:** EIA Short-Term Energy Outlook (March 10, 2026): "Brent crude oil spot price rose from an average of $71 per barrel (b) on February 27"
- **Confidence:** High (primary government source, exact date referenced)

### oil.wti
- **Old:** `70.82`
- **New:** `66.50`
- **Source:** FX Daily Report technical analysis (Feb 27, 2026): WTI trading $65.63–$66.52; session bounce to ~$66.52. Consistent with standard $4–5 Brent-WTI spread against $71 Brent.
- **Confidence:** Medium-high (triangulated from technical analysis and spread)

### gas.national_avg
- **Old:** `3.05`
- **New:** `2.98`
- **Source:** AAA weekly fuel report (Feb 26, 2026): "The national average for a gallon of regular gasoline went up by more than 5 cents this past week to $2.98"
- **Confidence:** High (AAA is the canonical source, report dated one day prior)

### markets.sp500
- **Old:** `6867`
- **New:** `6878.88`
- **Source:** CNBC market close (Feb 27, 2026): "The S&P 500 closed down 0.43% at 6,878.88"
- **Confidence:** Exact (verified closing price)

### markets.nasdaq
- **Old:** `22100`
- **New:** `22668.21`
- **Source:** CNBC market close (Feb 27, 2026): "Nasdaq Composite lost 0.92% to settle at 22,668.21"
- **Confidence:** Exact (verified closing price)

### markets.djia
- **Old:** `51300`
- **New:** `48977.92`
- **Source:** CNBC market close (Feb 27, 2026): "Dow Jones Industrial Average dropped 521.28 points, or 1.05%, to close at 48,977.92"
- **Confidence:** Exact (verified closing price)

### treasury.us_10yr_yield
- **Old:** `4.05`
- **New:** `3.97`
- **Source:** Advisor Perspectives Treasury Yields Snapshot (Feb 27, 2026): "The yield on the 10-year note finished February 27, 2026 at 3.97%, its lowest level in four months." Corroborated by FinancialContent: "on February 27, 2026, the yield dipped to 3.97% as a 'flight to safety' initially drove investors into government bonds"
- **Confidence:** Exact (two independent sources, exact date)

### treasury.dxy
- **Old:** `98.20`
- **New:** `97.57`
- **Source:** FX Daily Report (Feb 27, 2026): "US Dollar Index Pulls Back Off Session Highs to Trade at 97.57"
- **Confidence:** Medium-high (intraday snapshot, not confirmed close; close likely 97.5–98.0 range)

### commodities.gold_oz
- **Old:** `4980.00`
- **New:** `5236.00`
- **Source:** Fortune (Feb 27, 2026): "$5,226 per ounce as of 9:05 AM." FX Daily Report (Feb 27): "$5,236." Gold futures: $5,251.80. World Gold Council end-Feb: "$5,222/oz." Using FX Daily Report midpoint.
- **Confidence:** High (four sources converge in $5,222–$5,252 range; $5,236 is the best single-point estimate)

### commodities.silver_oz
- **Old:** `71.50`
- **New:** `92.06`
- **Source:** Fortune (Feb 27, 2026): "silver exchanged hands at $92.06 per ounce at 8:45 AM Eastern Time on February 27, 2026." Prior day (Feb 26) was $87.07. Silver had hit $121.67 ATH on Jan 29, 2026.
- **Confidence:** High (exact date, exact source)

### commodities.vix
- **Old:** `19.20`
- **New:** `19.86`
- **Source:** Cboe Index Insights (Feb 2026 monthly report): "The Cboe Volatility Index (the VIX® Index) gained more than two points to close at 19.86." Feb 27 was the last trading day of February.
- **Confidence:** High (official Cboe monthly report)

### defense_stocks.RTX
- **Old:** `128.50`
- **New:** `200.00`
- **Source:** RTX 52-wk high was $214.50 on 3/3/2026 after a ~4% war-rally. Pre-war price ~$200–206. Analyst consensus targets were $200–238 in late Feb. RTX entered 2026 at ~$185 and rallied on $1.5T defense budget proposal in early Jan.
- **Confidence:** Medium (estimated from war-rally reversal and analyst context; not a verified close)
- **Note:** Flag for direct verification via Yahoo Finance historical data if available.

### defense_stocks.LMT
- **Old:** `485.20`
- **New:** `647.00`
- **Source:** LMT hit record $692 on 3/2/2026 with a 7% surge. Backing out 7% from $692 = ~$647. Analyst target from Truist was $605 (set earlier). LMT was trading "near all-time high" pre-conflict per StockAnalysis.
- **Confidence:** Medium (derived from war-day surge percentage)
- **Note:** Flag for direct verification.

### defense_stocks.NOC
- **Old:** `520.80`
- **New:** `640.00`
- **Source:** NOC currently ~$735. NOC surged 5.8% in premarket on 3/2. Backing out ~8-10% total war rally from ~$700 range = ~$630-650. Analyst avg target was $541.36 (lagging, set before Jan rally). NOC gained 22% in 2025 plus 4%+ in early Jan 2026.
- **Confidence:** Medium (estimated)
- **Note:** Flag for direct verification.

### defense_stocks.GD
- **Old:** `298.40`
- **New:** `325.00`
- **Source:** GD currently ~$356. Surged ~5% premarket on 3/2 after ~5% decline day prior. Pre-war estimate ~$320–330.
- **Confidence:** Low-medium (estimated)
- **Note:** Flag for direct verification.

### defense_stocks.BA
- **Old:** `178.90`
- **New:** `200.00`
- **Source:** BA currently ~$218. Defense rally lifted it. Pre-war trajectory and 2026 price history suggest ~$195–210.
- **Confidence:** Low-medium (estimated)
- **Note:** Flag for direct verification.

### oil_stocks.XOM
- **Old:** `108.30`
- **New:** `122.00`
- **Source:** XOM currently ~$153, up 28% YTD and 41% past year. War-driven oil rally added substantial premium. Pre-war estimate ~$118–125 based on backing out post-Feb 28 surge.
- **Confidence:** Low-medium (estimated)
- **Note:** Flag for direct verification.

### oil_stocks.CVX
- **Old:** `152.60`
- **New:** `186.75`
- **Source:** Simply Wall St: "CVX closed at $186.75 on February 27." This is a verified closing price.
- **Confidence:** Exact (verified close, specific date cited)

### oil_stocks.COP
- **Old:** `112.40`
- **New:** `112.40`
- **Source:** Not independently verified. Flagged as suspect given systematic understatement across all equities. Leave as-is but mark for verification.
- **Confidence:** Unverified
- **Note:** Flag for direct verification.

---

## Fields Verified As-Is (No Change)

| Field | Value | Verification |
|---|---|---|
| `treasury.fed_funds_rate_upper` | `3.75` | Confirmed: Advisor Perspectives, FRED H.15 |
| `treasury.fed_funds_rate_lower` | `3.50` | Confirmed |
| `national_debt.debt_to_gdp_pct` | `100` | CBO projects crossing 100% around this period |
| `hormuz.daily_oil_flow_mbd` | `20.5` | EIA: "nearly 20% of global oil supply" ≈ 20 mbd |
| `hormuz.daily_tanker_transits` | `85` | Standard range 60–90; plausible |
| `humanitarian.*` | all zeros | Correct for pre-war baseline |

## Fields Requiring Minor Adjustment

| Field | Value | Adjustment | Reason |
|---|---|---|---|
| `national_debt.total_trillions` | `38.86` | → `38.73` | JEC: $38.56T on Feb 4, $38.86T on Mar 4. At $7.23B/day, Feb 27 ≈ $38.73T. Current value is the Mar 4 snapshot. |

## Airline Stocks — Unverified

All three airline values (`DAL: 62.50`, `UAL: 98.20`, `AAL: 17.80`) are unverified and suspect given the systematic understatement pattern across all equities. Leave unchanged but add a metadata flag or comment indicating they need verification from Yahoo Finance historical close data for 2026-02-27.

---

## Metadata Update

Update the `source` fields as follows:

- `oil.source`: `"EIA STEO (March 10, 2026) / FX Daily Report"`
- `gas.source`: `"AAA weekly fuel report (Feb 26, 2026)"`
- `markets.source`: `"CNBC market close reporting, Feb 27, 2026"`
- `treasury.source`: `"FRED DGS10 / Advisor Perspectives / FX Daily Report / Federal Reserve H.15"`
- `commodities.source`: `"Fortune daily commodity prices / FX Daily Report / Cboe Index Insights Feb 2026 / World Gold Council"`

Add a top-level `audit` object:

```json
"audit": {
  "date": "2026-03-14",
  "verified_closes": ["sp500", "nasdaq", "djia", "cvx", "us_10yr_yield", "vix"],
  "estimated_from_context": ["rtx", "lmt", "noc", "gd", "ba", "xom", "wti", "dxy"],
  "unverified": ["cop", "dal", "ual", "aal"],
  "primary_sources": [
    "EIA STEO March 10, 2026",
    "CNBC market close Feb 27, 2026",
    "Advisor Perspectives Treasury Snapshot Feb 27, 2026",
    "Cboe Index Insights February 2026",
    "AAA weekly fuel report Feb 26, 2026",
    "Fortune daily commodity prices Feb 27, 2026",
    "World Gold Council GRAM Feb 2026",
    "JEC Monthly Debt Update March 2026",
    "Simply Wall St CVX analysis"
  ]
}
```
