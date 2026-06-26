# Runbook — Sales prospecting & lead qualification

**Use when:** the user is in sales / business development ("find companies in sector X I can
approach", "is this lead worth my time", "list the biggest/healthiest firms in region Y").

## A. Build a prospect list
1. ONE `screen_companies` call: sector (NACE prefix) + region (postcode prefix) + a health
   floor (e.g. min solvency 0.30) + a size floor if relevant (min equity/EBITDA). Sort by size.
2. Present an **actionable list table**: name, n°, location, size proxy (equity / EBITDA /
   headcount), health (solvency). State the **total matches** and offer to refine.
3. Add a one-line **prioritisation**: who to approach first and why (size, health, growth).

## B. Qualify a single lead
1. `get_company(number)` → is it **big enough** (equity / EBITDA / FTE) and **healthy enough**
   (solvency, trend) to be worth the effort? Give a yes/no with the reason.
2. Surface **directors** (from the company file) as plausible contact points / decision-makers.

## Deliver
- For a list: a clean table sorted by relevance + "start with these 3".
- For a lead: a crisp **verdict** (worth it / marginal / skip) + size & health in one line +
  who to contact.
- Keep it practical and non-jargon; the user sells, they don't read balance sheets.

## Watch-outs
- Abbreviated accounts → no turnover; use equity / EBITDA / headcount as the size proxy.
- A long list isn't useful — qualify and rank, don't dump.
