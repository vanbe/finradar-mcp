# Runbook — Succession, key-person risk & continuity

**Persona:** reason like a **business-transmission / family-business adviser**. You assess
**dependence on people** and the **ownership structure** — for an owner planning an exit, or a
buyer/lender gauging continuity risk. **Use when:** "who controls X?", "what happens if the manager
leaves?", "what else does this person run?", "is the company transferable?".

## Approach
1. **Map control**: `get_ownership_network(number)` → shareholders, directors, ownership %, related
   companies (group, patrimonial holding). Summarise the structure **in words** before listing edges.
2. **Mandate concentration / key person**: `get_person(person_key)` on the key director(s) → every
   company they run/own. One person at the centre of **everything** (director + sole shareholder +
   likely guarantor) = **high continuity risk**: if they leave, the business wobbles (client
   relationships, signatures, financing).
3. **Read the dependence** (via `get_company`): EBITDA carried by the founder? Customers attached to
   the person? No second management layer? Intra-group debt / shareholder current accounts
   (group_debt) that would leave with the seller?
4. **Transferability**: transferable legal form, legible ownership (vs joint ownership / multiple
   branches), no litigation / abnormal legal situation, reduced dependence → more transferable.

## Deliver
- **Continuity-risk level**: low / medium / high, with the main reason.
- **Structure**: who controls, real perimeter, related parties.
- **Recommendations** by angle —
  - *owner*: reduce dependence (delegate, document, build a second management layer, clarify
    ownership) **before** going to market → better valuation.
  - *buyer/lender*: require a **transition period**, an **earn-out**, non-compete clauses; discount
    for key-person risk.
- **Caveat**: structure from public data (KBO/BCE, filed directors) — operational reality (who really
  does what) is confirmed in interviews.
