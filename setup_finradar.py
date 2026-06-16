#!/usr/bin/env python3
"""One-command setup for the FinRadar MCP server.

Run this ONCE, from the environment where this repo lives (Linux/macOS, or inside WSL on
Windows). It is deliberately dependency-free (standard library only) so it always runs:

    python3 setup_finradar.py frad_your_token_here
    # or, if you prefer to be prompted:
    python3 setup_finradar.py

What it does, in order, printing a clear result for each step:
  1. stores your token at ~/.finradar/token (chmod 600) — never inside the repo,
  2. smoke-tests the token against the live API (must return a company),
  3. installs the server's dependencies (mcp, httpx) into THIS Python,
  4. prints the exact command to register the "finradar" MCP server with Claude
     (and registers it automatically if the `claude` CLI is available).

It is safe to re-run. It changes nothing in git-tracked files.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent
DEFAULT_BASE_URL = "https://finradar.lab.vanbe.be"
TOKEN_FILE = Path.home() / ".finradar" / "token"


def say(ok: bool | None, msg: str) -> None:
    mark = "•" if ok is None else ("\033[32m✓\033[0m" if ok else "\033[31m✗\033[0m")
    print(f"  {mark} {msg}")


def fail(msg: str) -> None:
    print(f"\n\033[31mSetup stopped:\033[0m {msg}\n")
    sys.exit(1)


def get_token() -> str:
    for a in sys.argv[1:]:
        if a.startswith("frad_"):
            return a.strip()
    if os.environ.get("FINRADAR_TOKEN", "").strip():
        return os.environ["FINRADAR_TOKEN"].strip()
    try:
        tok = input("  Paste your FinRadar token (starts with frad_): ").strip()
    except EOFError:
        tok = ""
    if not tok:
        fail("no token provided. Generate one in FinRadar → profile → 'AI agent', then run "
             "`python3 setup_finradar.py frad_...`.")
    return tok


def base_url() -> str:
    return (os.environ.get("FINRADAR_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def store_token(tok: str) -> None:
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(tok)
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except OSError:
        pass
    say(True, f"token stored at {TOKEN_FILE} (read-only to you)")


def smoke_test(tok: str) -> None:
    url = f"{base_url()}/api/search?q=Colruyt&limit=1"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            fail("the token was rejected (401). It may be wrong or deleted — generate a fresh "
                 "one in FinRadar → profile → 'AI agent' and re-run this script.")
        fail(f"API error {e.code} from {base_url()}. Try again in a moment.")
    except Exception as e:  # noqa: BLE001
        fail(f"could not reach FinRadar at {base_url()} ({e}). Check your internet connection.")
    sample = (data.get("rows") or [{}])[0].get("name")
    say(True, f"token works — live API reachable ({base_url()})" + (f", e.g. “{sample}”" if sample else ""))


def ensure_deps() -> None:
    try:
        import mcp  # noqa: F401
        import httpx  # noqa: F401
        say(True, "server dependencies already present (mcp, httpx)")
        return
    except ImportError:
        pass
    say(None, "installing server dependencies (mcp, httpx)…")
    r = subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(REPO)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        # fall back to a plain dependency install (no packaging step)
        r = subprocess.run([sys.executable, "-m", "pip", "install", "mcp>=1.2", "httpx>=0.27"],
                           capture_output=True, text=True)
    if r.returncode != 0:
        say(False, "could not install dependencies automatically")
        print(r.stderr[-800:])
        fail("install them manually with: "
             f"{sys.executable} -m pip install mcp httpx   (then re-run this script)")
    say(True, "server dependencies installed")


def server_command() -> list[str]:
    """The command Claude should use to launch the server on THIS machine."""
    return [sys.executable, "-m", "finradar_mcp.server"]


def register(cmd: list[str]) -> bool:
    """Register with the Claude Code CLI if available. Returns True if it ran."""
    if "--no-register" in sys.argv or not shutil.which("claude"):
        return False
    subprocess.run(["claude", "mcp", "remove", "finradar", "--scope", "user"],
                   capture_output=True, text=True)
    r = subprocess.run(["claude", "mcp", "add", "finradar", "--scope", "user", "--", *cmd],
                       capture_output=True, text=True)
    if r.returncode == 0:
        say(True, "registered the 'finradar' MCP server with Claude (user scope)")
        return True
    say(False, "could not auto-register; use the manual command printed below")
    return False


def main() -> None:
    print("\n\033[1mFinRadar MCP — setup\033[0m")
    tok = get_token()
    store_token(tok)
    smoke_test(tok)
    ensure_deps()
    cmd = server_command()
    registered = register(cmd)

    pretty = " ".join(cmd)
    print("\n\033[1mYou're ready.\033[0m")
    if registered:
        print("  Reconnect the MCP server so the tools load now:")
        print("    • in Claude Code, run  /mcp  (or reopen this folder)")
    else:
        print("  Register the 'finradar' MCP server with Claude Code (one line):")
        print(f"      claude mcp add finradar --scope user -- {pretty}")
    # always show the exact launch command — needed if Claude Code runs on Windows but
    # this repo/Python live in WSL (wrap it: wsl.exe -e bash -lc "cd <repo> && exec <cmd>").
    print(f"\n  (launch command for this machine: {pretty})")
    print("\n  Then ask, in your own language, things like:")
    print("    • “How healthy is Colruyt Group, and is it stronger than five years ago?”")
    print("    • “Find IT companies with solvency above 50% and at least €1M equity.”")
    print("    • “Who controls enterprise 0400378485 — show the ownership structure?”\n")


if __name__ == "__main__":
    main()
