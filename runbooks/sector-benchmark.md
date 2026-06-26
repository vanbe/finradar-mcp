# Runbook — Sector benchmark & positioning

**Persona:** reason like a **strategy consultant / sector economist** (Bain / Roland Berger style).
You position a company **against its peers**, in ranges, not absolutes.
**Use when:** "how does X compare in its sector?", "what are sector Y's margins?", "is this a good
margin for this trade?", "who are the leaders in this sector/region?".

## Approach
1. **Identify the target & its trade**: `get_company(number)` → NACE, size (turnover/EBITDA/equity),
   margins. Note the **schema** (abbreviated → turnover often undisclosed → margins not comparable;
   say so).
2. **Build a peer panel**: `screen_companies` on the **same NACE prefix**, relevant region, and a
   **comparable size band** (`min_*`/`max_*` around the target — a benchmark only makes sense at
   similar size; don't compare an SME to a multinational). Sort by EBITDA or margin. Pull a
   representative sample.
3. **Compare the right ratios** (fractions → show as %): gross / EBITDA / net margin, solvency, ROE,
   revenue growth. Give a **median / range** for the panel.
4. **Position the target**: above / within / below the peer range, and **why** (size effect,
   integration, mix, price positioning).

## Deliver
- **One-line positioning** (e.g. "12% EBITDA margin = top quartile of its NACE in Wallonia").
- **Table**: target vs panel median on 3–4 key ratios.
- **Reading**: what the gap reveals (cost advantage, brand premium, underperformance to fix) + one
  action or deeper-dive lead.
- **Honest caveat**: the sample = **companies that disclose turnover** (full schema); abbreviated
  filings (most SMEs) are absent → indicative, not exhaustive. State the panel size.
