# Runbook — Indicative valuation

**Use when:** the user asks what a company is worth, a sale/exit range, or "value X on an
EBITDA multiple". Owners, fiduciaries advising a sale, buyers cross-checking a price.

## Steps
1. `get_company(number)` → most recent **EBITDA** (and its trend), **net debt** (total debt −
   cash), equity, and any 🔴 legal signal.
2. Pick a **sector EBITDA multiple range** (rule of thumb ~4–8×): lower end for small,
   cyclical, declining or highly levered; higher end for growing, asset-light, resilient.
3. Enterprise value = EBITDA × multiple. **Equity value = EV − net debt.** Compute a low and a
   high.

## Deliver
- A **range** (e.g. "~€X–€Y for the equity"), the **multiple and EBITDA** used, and the
  **net-debt bridge** — explicitly.
- The **assumptions** (which multiple, why) and what would move the number.
- Caveats: indicative only; private SMEs are illiquid (discount), abbreviated accounts limit
  precision, one-off items distort EBITDA. **Not a formal valuation or fairness opinion.**

## Don't
- Don't give a single point value. Don't value on net result alone. Don't invent a multiple
  without naming it.
