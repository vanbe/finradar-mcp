# Runbook — Credit check / counterparty risk

**Use when:** the user wants to decide whether to extend credit, onboard a supplier/customer,
or judge whether a company is a reliable counterparty ("is X safe to work with / to give 30-day
terms / to grant €X credit?"). Typical for accountants, fiduciaries, procurement, finance teams.

## Steps
1. `get_company(number)` (use `search_companies` first if you only have the name).
2. **Legal-situation gate first.** If the company is in bankruptcy, liquidation or judicial
   reorganisation → that's a 🔴 red flag; say it up front, it overrides the ratios.
3. Read the FinRadar **credit score** + **solvency** (equity/assets), **current ratio**
   (liquidity), **net result and its trend**, and **leverage** (debt ratio). Negative or thin
   equity = fragile.
4. Look at the multi-year **direction**: improving vs deteriorating matters as much as the level.

## Deliver
- A clear **verdict**: 🟢 favourable / 🟠 watch / 🔴 risky — one sentence of why.
- A suggested **credit ceiling**: a prudent fraction of equity (and never more than the
  counterparty can plausibly service from EBITDA). State it as a range.
- If 🟠: **mitigations** — shorter terms, partial prepayment, a guarantee, periodic re-check.
- Source line: *(NBB filings, <years>)* + link to the company page.
- Caveat: this is analysis, **not an official credit rating**.

## Watch-outs
- Abbreviated accounts disclose less (no turnover) → say what you can and can't conclude.
- One good year after losses ≠ recovery; weight the trend.
