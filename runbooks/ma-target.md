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

## A. Sourcing a shortlist — **size a FINANCEABLE target first**
⚠️ Classic mistake: sorting `order_by=ebitda` with **no size ceiling** → you surface the BIGGEST
companies in the area (multinationals) the buyer cannot finance. And the **buyer's equity budget is
NOT a `min_equity` on the target** (don't confuse the acquirer's capital with the target's equity).

**Compute the affordable price range first**, then translate it into size caps:
1. **Buying power** ≈ buyer's equity ÷ the equity share of the structure. An SME LBO is typically
   **30–50% equity** + bank debt (≈ 3–4× EBITDA) + possible vendor loan / regional subsidy. So:
   - **Affordable enterprise value (EV) ≈ equity ÷ 0.3 to 0.5.**
     *E.g. €200k equity → EV ≈ €0.4–0.7M* (top of range with vendor loan / subsidy).
2. **Translate EV to target EBITDA**: EV ≈ EBITDA × **4–6×** ⇒ **target EBITDA ≈ EV ÷ 5**.
   *E.g. EV €0.4–0.7M → EBITDA ≈ €80–150k.* Use a wide band.
3. **Parameterise the screen with UPPER bounds** (the key point):
   - `acquirable_only=true`; `exclude_distressed=true` (unless distressed mandate).
   - `min_ebitda` ≈ low end (profitable, e.g. €50–75k) AND **`max_ebitda` ≈ high end** (e.g.
     €200–300k) — without this ceiling you get giants.
   - **`max_equity`** to drop very large balance sheets (e.g. ≤ €1–2M equity).
   - `nace` (sector) and `zipcode` (region) per the request.
   - `min_solvency` ≈ 0.25–0.30 to avoid over-leveraged firms.
   - `order_by=ebitda` is still fine, but **`max_ebitda`/`max_equity` is what guarantees affordability**.
4. Too few results → widen the bounds once; too many → tighten. Explain the bounds and **why**
   (the financing structure), not just the list.
5. Each row carries `legal_form` and `distress` (legal situation if not normal).
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
