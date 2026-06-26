# Runbook — M&A target (sourcing, due diligence, valuation)

**Use when:** the user is a buy-side / acquirer / deal-sourcer ("find acquisition targets",
"analyse X as a target", "what's it worth", "who controls it").

## A. Sourcing a shortlist
1. ONE well-parameterised `screen_companies` call: sector (NACE prefix), region (postcode
   prefix), thresholds (min solvency, min equity/EBITDA). Sort by EBITDA or equity.
2. Present a **shortlist table** (name, n°, region, size, EBITDA, solvency) and state the
   **total matches** behind the sample. Offer to narrow (size band, profitability, region).

## B. Due diligence on a named target
1. `get_company(number)` → health, multi-year **trend**, **leverage** (debt ratio), margins,
   legal situation. Flag deterioration and any 🔴 legal signal.
2. `get_ownership_network(number)` → who controls it and **what else the owner holds** (group,
   carve-out potential, related-party risk).

## C. Indicative valuation
- Enterprise value ≈ **EBITDA × sector multiple** (rule of thumb ~4–8×; lower for small,
  cyclical, declining or highly levered; higher for growing, asset-light, resilient).
- Equity value ≈ EV − **net debt** (total debt − cash).
- Give a **range** (low/high multiple) and **state the assumptions**. Never a single point.

## Deliver
- One-line thesis (attractive / mixed / pass) + the 3 figures that drive it.
- Key **risks** (trend, leverage, customer/owner concentration, legal).
- A suggested **next step** (request management accounts, confirm normalised EBITDA, etc.).
- Caveat: indicative analysis on public filings, not a fairness opinion.
