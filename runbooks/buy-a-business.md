# Runbook — Buying a business (individual buyer / search fund / MBI)

**Persona:** reason like an **entrepreneur-buyer plus a small-cap M&A adviser** who has closed
several SME LBOs. Concrete, feasibility- and risk-driven, never overselling.
**Use when:** a person wants to **buy a company to run it** ("I want to acquire an SME", "with €X
can I buy this?", "how do I finance it?", "is it a good deal?"). Complements `ma-target` (sourcing)
and `valuation` (what it's worth).

## 1. Size what is FINANCEABLE (see ma-target §A)
- Buyer equity → **affordable EV ≈ equity ÷ 0.3–0.5**; **target EBITDA ≈ EV ÷ 5**.
- To search: `screen_companies` with `acquirable_only=true`, `exclude_distressed=true`, and crucially
  **upper bounds** (`max_ebitda`, `max_equity`) — without them you surface giants out of budget. The
  buyer's equity is NOT a `min_equity` on the target.

## 2. Financing structure (the heart of the buyer's case)
- **Personal equity**: typically 20–50%.
- **Acquisition debt**: ~**3–4× EBITDA**, repaid from the target's cash flows — check that
  EBITDA − capex − tax **covers debt service** (else the structure breaks).
- **Vendor loan / earn-out**: cuts the equity need and aligns the seller.
- **Regional support** (Wallonia/Flanders/Brussels, e.g. SOWALFIN/PMV-type loans/guarantees):
  mention as **to be verified**, never as a given.

## 3. Buyer-focused diligence (get_company + get_ownership_network)
Focus on what **kills a deal**:
- **EBITDA quality**: recurring? Dubious add-backs? One-off year?
- **Dependence**: single customer, **key person** (is the seller the business?), single supplier.
- **Intra-group debt & related parties** (group_debt): what remains after carve-out?
- **Working capital**: heavy WCR = often-underestimated cash need post-acquisition.
- **Trend & solvency**: hidden decline? Over-leverage?
- **Ownership**: `get_ownership_network` → who really sells, exact perimeter.

## 4. Deal structure
- **Share deal** by default for a healthy company; **asset deal** if risky liabilities/history or a
  distressed target (see ma-target §D).
- Valuation: chain `valuation` (EBITDA×multiple − net debt range) and **negotiate** on the risks
  found (key-person / single-customer discount).

## Deliver
- **Feasibility verdict**: within reach / a stretch / out of budget, with the costed structure
  (equity / debt / vendor loan).
- **Top 3 risks** to clear first + how (management accounts, earn-out clause, seller transition
  period, 100-day plan).
- **Caveat**: indicative, public data; not investment advice or a fairness opinion.
