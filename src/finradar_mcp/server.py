"""FinRadar MCP server.

Exposes the FinRadar financial-intelligence API (Belgian companies — KBO/BCE identity +
NBB/BNB annual accounts) as Model Context Protocol tools, so a Claude agent can answer
questions in plain language with grounded, sourced figures.

Auth: a personal API token generated in the FinRadar web app (profile → "AI agent").
The token is read from the FINRADAR_TOKEN environment variable, or from ~/.finradar/token.

Every figure returned traces back to an official source: company identity from the Belgian
Crossroads Bank for Enterprises (KBO/BCE), financials from annual accounts filed at the
National Bank of Belgium (NBB/BNB). Each company has a public page at <base>/e/<number>.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

DEFAULT_BASE_URL = "https://finradar.lab.vanbe.be"
TOKEN_FILE = Path.home() / ".finradar" / "token"

mcp = FastMCP("finradar")


def _base_url() -> str:
    return (os.environ.get("FINRADAR_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def _token() -> str:
    tok = os.environ.get("FINRADAR_TOKEN", "").strip()
    if not tok and TOKEN_FILE.exists():
        tok = TOKEN_FILE.read_text().strip()
    if not tok:
        raise RuntimeError(
            "No FinRadar token found. Generate one in the FinRadar web app "
            "(profile → 'AI agent'), then set FINRADAR_TOKEN or write it to ~/.finradar/token."
        )
    return tok


def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    """GET a FinRadar API endpoint with the personal token. Clean error messages for the model."""
    clean = {k: v for k, v in (params or {}).items() if v is not None}
    try:
        r = httpx.get(
            f"{_base_url()}{path}",
            params=clean,
            headers={"Authorization": f"Bearer {_token()}"},
            timeout=30.0,
        )
    except httpx.HTTPError as e:
        raise RuntimeError(f"Could not reach FinRadar ({_base_url()}): {e}") from e
    if r.status_code == 401:
        raise RuntimeError("FinRadar rejected the token (401). It may be wrong, revoked, or not set.")
    if r.status_code == 404:
        return None
    if r.status_code >= 400:
        raise RuntimeError(f"FinRadar API error {r.status_code}: {r.text[:200]}")
    return r.json()


def _fiche_url(number: str) -> str:
    return f"{_base_url()}/e/{number}"


# ─────────────── formatting → analysis-ready output (no client-side code needed) ───────────────
def _eur(v) -> str:
    if v is None:
        return "—"
    n = float(v)
    a = abs(n)
    if a >= 1e9:
        return f"€{n / 1e9:.2f}bn"
    if a >= 1e6:
        return f"€{n / 1e6:.1f}m"
    if a >= 1e3:
        return f"€{n / 1e3:.0f}k"
    return f"€{n:.0f}"


def _pct(v) -> str:
    return "—" if v is None else f"{float(v) * 100:.1f}%"


def _ratio(v) -> str:
    return "—" if v is None else f"{float(v):.2f}"


def _num(v) -> str:
    return "—" if v is None else f"{float(v):,.0f}"


def _days(v) -> str:
    return "—" if v is None else f"{float(v):.0f}d"


_FMT = {"eur": _eur, "pct": _pct, "ratio": _ratio, "num": _num, "days": _days}

# curated rows for the multi-year table (key, label, kind) — the headline figures an analyst reads
_TABLE_ROWS = [
    ("employees", "Employees (FTE)", "num"),
    ("turnover", "Turnover", "eur"),
    ("ebitda", "EBITDA", "eur"),
    ("ebit", "EBIT", "eur"),
    ("net_result", "Net result", "eur"),
    ("equity", "Equity", "eur"),
    ("total_assets", "Total assets", "eur"),
    ("total_debt", "Total debt", "eur"),
    ("cash", "Cash", "eur"),
    ("working_capital", "Working capital", "eur"),
    ("dividends", "Dividends", "eur"),
    ("solvency", "Solvency", "pct"),
    ("debt_ratio", "Debt ratio", "pct"),
    ("current_ratio", "Current ratio", "ratio"),
    ("roe", "ROE", "pct"),
    ("roa", "ROA", "pct"),
    ("net_margin", "Net margin", "pct"),
]
_MAX_TABLE_YEARS = 6


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    return "\n".join([head, sep, body])


def _financials_table(trend: list[dict]) -> str | None:
    """Pre-rendered multi-year table (metrics as rows, recent years as columns) so the model can
    present it directly without writing any formatting code."""
    if not trend:
        return None
    years = trend[:_MAX_TABLE_YEARS]                       # trend is newest-first
    headers = ["Metric"] + [str(y.get("year")) for y in years]
    rows = []
    for key, label, kind in _TABLE_ROWS:
        if all(y.get(key) is None for y in years):
            continue                                       # skip rows with no data at all
        rows.append([label] + [_FMT[kind](y.get(key)) for y in years])
    acct = [str(y.get("account_type") or "—") for y in years]
    rows.append(["Accounts model"] + acct)
    return _markdown_table(headers, rows)


# ─────────────────────────────── tools ───────────────────────────────
@mcp.tool()
def search_companies(query: str, limit: int = 20) -> dict:
    """Search Belgian companies and people by name.

    Use this first when the user names a company or a person but you don't have its
    enterprise number. Returns matching companies (with their 10-digit enterprise number,
    legal form and city) and matching individuals (directors/owners, with how many
    companies they are linked to). Feed an enterprise number into `get_company` for the
    full financial file.

    Args:
        query: part of a company or person name (min 2 characters), e.g. "Colruyt".
        limit: max results per category (1–100).
    """
    d = _get("/api/search", {"q": query, "limit": max(1, min(limit, 100))})
    if not d:
        return {"query": query, "companies": [], "people": []}
    companies = [
        {
            "enterprise_number": r["enterprise_number"],
            "name": r.get("name"),
            "legal_form": r.get("juridical_form"),
            "is_person": r.get("toe") == "1",
            "city": " ".join(x for x in [r.get("zipcode"), r.get("municipality")] if x) or None,
            "page": _fiche_url(r["enterprise_number"]),
        }
        for r in d.get("rows", [])
    ]
    people = [
        {
            "person_key": p["person_key"],
            "name": " ".join(x for x in [p.get("firstname"), p.get("surname")] if x),
            "n_companies": p.get("n_companies"),
        }
        for p in d.get("particuliers", [])
    ]
    return {"query": query, "companies": companies, "people": people,
            "source": "KBO/BCE company register"}


@mcp.tool()
def screen_companies(
    nace: str | None = None,
    zipcode: str | None = None,
    min_solvency: float | None = None,
    min_equity: float | None = None,
    min_current_ratio: float | None = None,
    min_ebitda: float | None = None,
    max_ebitda: float | None = None,
    situation: str | None = None,
    acquirable_only: bool = False,
    exclude_distressed: bool = False,
    order_by: str = "ebitda",
    desc: bool = True,
    limit: int = 25,
) -> dict:
    """Find companies matching financial and sector criteria (a screen / lead list).

    This is the tool for questions like "profitable construction firms near Liège" or
    "companies with solvency above 50% and equity over €1M". Filters are combined (AND).
    Only companies that file annual accounts (legal entities) are screened.

    Args:
        nace: activity code PREFIX (NACE 2025). Sector divisions, e.g. "41","42","43" =
            construction, "62" = IT services, "10"/"11" = food/drink, "47" = retail,
            "68" = real estate, "70" = head-office/consulting, "86" = health. A prefix
            like "43" matches every sub-class 43xx.
        zipcode: Belgian postal-code PREFIX. "4" or "40" = Liège region, "1000" = Brussels
            centre, "10" = Brussels region, "20"/"21" = Antwerp, "9" = East Flanders.
        min_solvency: minimum solvency ratio as a fraction (0.5 = 50% equity/assets).
        min_equity: minimum equity in euros (e.g. 1000000 for €1M).
        min_current_ratio: minimum current ratio (current assets / short-term debt).
        min_ebitda / max_ebitda: EBITDA bounds in euros.
        situation: "abnormal" for companies in any non-normal legal situation (bankruptcy,
            dissolution, …) — useful for distress screens. Omit for normal companies.
        acquirable_only: True for an M&A target screen — excludes legal forms that cannot be
            bought (no transferable share capital / non-profit / public): non-profits (ASBL/VZW),
            foundations, mutual insurers, professional unions, public-law bodies, CPAS, religious
            establishments, co-ownerships, foreign associations… Keeps SRL/BV, SA/NV, SC/CV, etc.
        exclude_distressed: True to drop companies in distress (bankruptcy, dissolution /
            liquidation, judicial reorganisation / moratorium). Use for an M&A target screen unless
            the user explicitly wants distressed / turnaround opportunities. Each returned row also
            carries `legal_form` and `distress` (the legal situation when not normal — flag it).
        order_by: one of "ebitda","equity","net_result","total_assets","employees","name",
            "zipcode","year". Default "ebitda".
        desc: True for descending (largest first), False for ascending.
        limit: number of companies to return (1–200).

    Returns the matching companies with their latest-year key figures, plus the total
    number of matches behind the limit.
    """
    params = {
        "nace": nace, "zipcode": zipcode, "min_solvency": min_solvency,
        "min_equity": min_equity, "min_current_ratio": min_current_ratio,
        "min_ebitda": min_ebitda, "max_ebitda": max_ebitda, "situation": situation,
        "acquirable_only": acquirable_only, "exclude_distressed": exclude_distressed,
        "order_by": order_by, "desc": desc, "limit": max(1, min(limit, 200)),
        "include_all": False,
    }
    d = _get("/api/screen", params)
    if not d:
        return {"matches": [], "total": 0}
    rows = [
        {
            "enterprise_number": r["enterprise_number"],
            "name": r.get("name"),
            "legal_form": r.get("form_label") or r.get("juridical_form"),
            # distress = legal situation when NOT normal (bankruptcy, liquidation, reorg) → flag it.
            "distress": r.get("situation_label") if (r.get("situation") or "000") != "000" else None,
            "city": " ".join(x for x in [r.get("zipcode"), r.get("municipality")] if x) or None,
            "year": r.get("year"),
            "employees": r.get("employees"),
            "equity_eur": r.get("equity"),
            "total_assets_eur": r.get("total_assets"),
            "net_result_eur": r.get("net_result"),
            "ebitda_eur": r.get("ebitda"),
            "accounts_model": r.get("account_type"),
            "legal_situation": r.get("situation_label"),
            "page": _fiche_url(r["enterprise_number"]),
        }
        for r in d.get("rows", [])
    ]
    table = None
    if rows:
        headers = ["#", "Company", "Nr", "City", "Yr", "EBITDA", "Net result", "Equity", "FTE"]
        trows = [[
            str(i), (r["name"] or "—")[:40], r["enterprise_number"], (r["city"] or "—")[:24],
            str(r["year"] or "—"), _eur(r["ebitda_eur"]), _eur(r["net_result_eur"]),
            _eur(r["equity_eur"]), _num(r["employees"]),
        ] for i, r in enumerate(rows, 1)]
        table = _markdown_table(headers, trows)
    return {
        "table": table,                      # ready to present; amounts in EUR (m/bn scaled)
        "matches": rows,                     # full structured rows for custom use
        "returned": len(rows),
        "total_matches": d.get("total"),
        "ordered_by": order_by + (" desc" if desc else " asc"),
        "notes": "`table` is pre-formatted — present it directly. `total_matches` is the full "
                 "count behind the returned sample; offer to refine or sort if it's large.",
        "source": "NBB/BNB annual accounts (latest filed year per company)",
    }


@mcp.tool()
def get_company(number: str) -> dict:
    """Get the full financial file of one Belgian company by its enterprise number.

    Use after `search_companies` (or when the user gives a 10-digit number). Returns
    identity (name, legal form, status, address, activities), the multi-year history of
    key figures AND ratios (equity, total assets, debt, EBIT/EBITDA, net result, turnover,
    margins, solvency, current ratio, ROE/ROA, DSO/DPO, headcount…), the people and
    companies connected to it (directors and shareholders), and the list of filed annual
    accounts. Every number comes from official NBB/BNB filings.

    The result includes `financials_table`: a ready-to-present Markdown table (recent years ×
    headline metrics, already formatted). Present it directly — no need to write code to parse
    or reformat the output. `financials_by_year` holds the full structured history for custom
    calculations or older years.

    Args:
        number: the 10-digit enterprise number (digits only, e.g. "0400378485").
    """
    num = "".join(c for c in number if c.isdigit())
    d = _get(f"/api/enterprise/{num}")
    if not d:
        return {"error": f"No company found for enterprise number {num}."}
    info = d.get("info") or {}
    addr = d.get("address") or {}
    address = " ".join(x for x in [addr.get("street"), addr.get("house_number")] if x)
    if addr.get("zipcode") or addr.get("municipality"):
        address += ", " + " ".join(x for x in [addr.get("zipcode"), addr.get("municipality")] if x)
    relations = [
        {
            "party": r.get("party_label"),
            "party_number": r.get("party_kbo"),
            "link": ("owns / shareholder" if r.get("nature") == "ownership" else "director/control"),
            "role": r.get("role"),
            "direction": ("of this company" if r.get("direction") == "in" else "this company → them"),
            "stake_pct": round(r["pct"] * 100, 1) if r.get("pct") is not None else None,
            "active": r.get("active"),
        }
        for r in (d.get("relations") or [])
    ]
    documents = [
        {"year": doc.get("period_end_year"), "model": doc.get("model_name"),
         "filed": str(doc.get("deposit_date") or "") or None}
        for doc in (d.get("documents") or [])
    ]
    return {
        "identity": {
            "enterprise_number": info.get("enterprise_number", num),
            "name": info.get("name"),
            "legal_form": info.get("juridical_form"),
            "status": info.get("status"),
            "legal_situation": info.get("situation_label"),
            "is_natural_person": info.get("type_of_enterprise") == "1",
            "start_date": str(info.get("start_date") or "") or None,
            "address": address.strip(", ") or None,
            "main_activity": (f"{d['nace']['nace_code']} — {d['nace'].get('description') or ''}"
                              if d.get("nace") else None),
            "activities": [f"{a['nace_code']} ({a['nace_version']}, {a['classification']})"
                           f"{' — ' + a['label'] if a.get('label') else ''}"
                           for a in (d.get("activities") or [])],
            "linkedin": d.get("linkedin"),
            "page": _fiche_url(num),
        },
        # ready-to-present table (recent years × headline metrics) — no formatting code needed
        "financials_table": _financials_table(d.get("trend") or []),
        # full structured history (newest-first), raw numbers in EUR / fractions, for custom asks
        "financials_by_year": d.get("trend") or [],
        "connections": relations,
        "filed_accounts": documents,
        "notes": "Amounts in EUR; ratios are fractions (0.41 = 41%); employees = average FTE. "
                 "`financials_table` is pre-formatted (last 6 years) — present it directly. Use "
                 "`financials_by_year` only for older years or custom calculations.",
        "source": "Identity: KBO/BCE · Figures & ratios: NBB/BNB annual accounts. "
                  "Ratios are computed from official balance-sheet lines; open the company "
                  "page to export an Excel with the underlying formulas.",
    }


@mcp.tool()
def get_ownership_network(entity: str, depth: int = 1) -> dict:
    """Map who controls/owns a company and what it owns — the relationship graph.

    Use for "who is behind ACME?", "what else does this owner control?", group structure.
    Returns nodes (companies and people) and directed edges: "control" (director mandates)
    and "owns" (shareholdings, with %). Center on a company (10-digit number) or a person
    (person_key from `search_companies`).

    Args:
        entity: enterprise number (company) or person_key (individual) to center on.
        depth: how many hops to expand (1–3). Start at 1; raise to 2 to reach the wider
            group. Higher depth returns more nodes.
    """
    d = _get("/api/graph", {"center": entity.strip(), "depth": max(1, min(depth, 3))})
    if not d:
        return {"error": f"Unknown entity '{entity}'."}
    return {
        "center": d.get("center"),
        "nodes": [{"id": n["id"], "type": n.get("type"), "name": n.get("label"),
                   "legal_form": n.get("form"), "legal_situation": n.get("situation_label")}
                  for n in d.get("nodes", [])],
        "edges": [{"from": e["source"], "to": e["target"], "link": e["kind"],
                   "detail": e.get("label"), "active": e.get("active")}
                  for e in d.get("edges", [])],
        "source": "Directors & shareholders from KBO/BCE publications.",
    }


@mcp.tool()
def get_person(person_key: str) -> dict:
    """Get the profile of an individual: the companies they direct and/or own.

    Use with a person_key returned by `search_companies` to see someone's mandates and
    holdings across Belgian companies (useful for succession/owner-risk questions).

    Args:
        person_key: the person key from `search_companies` (not a company number).
    """
    d = _get("/api/person", {"key": person_key.strip()})
    if not d:
        return {"error": f"Unknown person '{person_key}'."}
    return d


def main() -> None:
    """Console entry point — runs the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
