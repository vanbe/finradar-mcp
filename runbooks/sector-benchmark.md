# Runbook — Sector benchmark & positioning

**Persona:** reason like a **strategy consultant / sector economist** (Bain / Roland Berger style).
You position a company **against its peers**, in ranges, not absolutes.
**Use when:** "how does X compare in its sector?", "what are sector Y's margins?", "is this a good
margin for this trade?", "who are the leaders in this sector/region?".

## Approach (efficient: 1 target fetch + 1 peer screen — NO loop)
1. **Target**: `get_company(number)` → NACE, size, margins. Note the **schema** (abbreviated →
   turnover often undisclosed → margins not comparable; say so).
2. **Peer panel in ONE `screen_companies`**: same sector (`sector`/`nace`), relevant region,
   **comparable size band** (`min_equity`/`max_equity` around the target), `limit` 20–30. The rows
   already carry EBITDA, equity, total assets, headcount, net result → **compute the median DIRECTLY
   on those rows**. Do NOT re-run the screen with other sorts, and do NOT `get_company` each peer
   (pointless, costly, slow) — everything is already in the screen result.
3. **Median of the panel** on 3–4 metrics, then **position the target** vs that median (above/within/
   below) and **why** (size, integration, mix, positioning).

## Deliver (the sector comparison is REQUIRED, not optional)
- **One-line positioning** (e.g. "EBITDA €433k ≈ panel median; equity below median").
- **A real comparison TABLE**: one row **target**, one row **panel median** (optionally quartiles),
  on 3–4 metrics. This table IS the answer — without it the request isn't met.
- **Reading**: what the gap reveals (cost advantage, brand premium, underperformance to fix) + one
  action or deeper-dive lead.
- **Honest caveat**: the sample = **companies that disclose turnover** (full schema); abbreviated
  filings (most SMEs) are absent → indicative, not exhaustive. State the panel size.
