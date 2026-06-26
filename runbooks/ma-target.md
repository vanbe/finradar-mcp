# Runbook — M&A target (sourcing, due diligence, valuation)

**Use when:** the user is a buy-side / acquirer / deal-sourcer ("find acquisition targets",
"analyse X as a target", "what's it worth", "who controls it"). Posture: rigorous M&A advisor
(due-diligence mindset), factual, never overselling. Every figure must come from a tool.

## Guiding principle: what is an *acquirable* target?
An acquisition = buying the **shares** (share deal) or the **assets** (asset deal) of an entity
with **transferable capital** that **actually operates** and is **not dying**. Two non-negotiable
filters apply before any analysis:

1. **Transferable legal form.** EXCLUDE entities with no share capital to buy or that are
   non-profit / public: non-profits (ASBL/VZW, AISBL/IVZW), foundations, mutual insurers,
   professional unions, mutual-insurance associations, (con)federations, professional orders,
   co-ownerships, religious establishments, CPAS/OCMW, public-law bodies & legal persons, public
   services, foreign associations, entities with no Belgian seat. → always `acquirable_only=true`.
   Typical targets remain: **SRL/BV, SA/NV, SC/CV, SComm** and assimilated commercial forms.
2. **Not in distress (by default).** EXCLUDE bankruptcy, dissolution/liquidation, moratorium,
   **judicial reorganisation**. → `exclude_distressed=true` by default.
   *Exception:* if the user explicitly wants **distressed / turnaround / asset pick-up**, keep them
   but handle separately (see § D).

## A. Sourcing a shortlist
1. **ONE** well-parameterised `screen_companies` call:
   - `acquirable_only=true` **always**; `exclude_distressed=true` unless an explicit distressed mandate.
   - sector (`nace` prefix), region (`zipcode` prefix), thresholds (`min_solvency`, `min_equity`,
     `min_ebitda`). For a buyer with €X of equity, size `min_ebitda`/`min_equity` to a target the
     buyer can realistically finance (order of magnitude, not a hard rule).
   - Sort by `ebitda` (earnings power) or `equity`.
2. Each row carries `legal_form` and `distress` (legal situation if not normal).
   **If `distress` is set on a row** (only possible under a distressed mandate): mark it **🔴
   explicitly** in the table; never present it as a healthy target.
3. Present a **shortlist table** (name, n°, region, size, equity, solvency, form) and state the
   **total matches** behind the sample. Offer to narrow (size band, profitability, region).

## B. Due diligence on a named target
1. `get_company(number)` → health, multi-year **trend** (turnover/EBITDA/result), **leverage**
   (net debt / equity), margins, **credit score**, **legal situation**.
   - Check the **form** (transferable?) and **situation**: any bankruptcy / liquidation / judicial
     reorganisation = **🔴 red flag at the top of the answer**, never buried.
   - Distinguish an **operating company** (recurring EBITDA, headcount) from a **holding / asset /
     real-estate company** (little EBITDA, large balance sheet): valuation and thesis differ (§ C).
2. `get_ownership_network(number)` → who controls it and **what else the owner holds** (group,
   related-party risk, the real perimeter to buy, likely carve-out).

## C. Indicative valuation
Computed **on the fly**, with the **formula shown** next to the result (transparency; the multiple
is a contextual judgement, not a fixed constant). Method:

- **Enterprise value (EV) ≈ normalised EBITDA × sector multiple.** Multiple ~**4–8×**:
  low (3–5×) for small / cyclical / declining / single-customer / highly levered;
  high (6–8×+) for growing / recurring / asset-light / resilient / niche leader.
- **Equity value ≈ EV − net debt** (financial debt − cash).
- **Asset/real-estate company:** reason on **NAV** (net asset value: equity adjusted for latent
  gains/losses on assets), not an EBITDA multiple.
- Always a **range** (low→high multiple) and **state the assumptions** (EBITDA used, net debt
  estimate, multiple and why). **Never a single point.**
- *Discount* for: key-person dependence, single customer, stale data, uncertain add-backs.

Example: "EV ≈ EBITDA €1.2M × 4–6× = **€4.8–7.2M**; − net debt ~€0.8M ⇒ **equity value ≈ €4.0–6.4M**
(assumptions: unnormalised EBITDA, net debt estimated from the latest balance sheet)."

## D. Distressed case (only on an explicit mandate)
- Often prefer an **asset deal** (buying the business / selected assets) over a **share deal**: avoid
  inheriting the liabilities and history of an entity under proceedings.
- Valuation **≠ EBITDA multiple**: reason on **liquidation / asset value**, working capital, and
  turnaround cost. Flag the risks (going concern, employee liabilities, securities/pledges).

## Deliver
- **One-line thesis** (attractive / mixed / pass) + the **3 figures** that drive it.
- **Flags**: 🔴 distress / non-transferable form if applicable, at the TOP.
- Key **risks** (trend, leverage, customer/owner concentration, key-person, legal).
- A suggested **next step** (management accounts, normalise EBITDA, data room…).
- Caveat: indicative analysis on public filings, not a fairness opinion or investment advice.
  Mention any region-linked subsidies (Wallonia/Flanders/Brussels) as **to be verified**, not a given.
