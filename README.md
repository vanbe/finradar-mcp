# FinRadar MCP — chat with Belgian company data

Ask questions about Belgian companies **in plain language**, straight from your own Claude:
*"Is ACME financially healthy?"*, *"Find profitable construction firms near Liège"*,
*"Who controls this company, and what else do they own?"* — and get a clear, **sourced**
answer where every figure traces back to the official filing (KBO/BCE + National Bank of
Belgium).

This little project connects Claude to FinRadar through an **MCP server**. You don't need to
be technical: you copy a token, open Claude, paste it, and Claude sets everything up for you.

> 🇫🇷 **Version française plus bas** ·  🇬🇧 English first.

---

## 🇬🇧 Get started in 4 steps (~5 minutes)

**What you need**
- A **FinRadar account** (the web app your class uses).
- **Claude Code** (recommended) — or Claude Desktop. Either is fine.
- 5 minutes. No coding.

### 1. Get this project onto your computer
- **Easiest:** download the ZIP →
  **[Download finradar-mcp](https://github.com/vanbe/finradar-mcp/archive/refs/heads/main.zip)**,
  then unzip it. You'll get a folder named `finradar-mcp`.
- **Or**, if you use git:
  ```
  git clone https://github.com/vanbe/finradar-mcp.git
  ```

### 2. Get your personal token
1. Log in to **FinRadar** in your browser.
2. Click your **name/profile** (top-right) → **🤖 AI agent (token)**.
3. Click **Generate a token** and **copy** it (it starts with `frad_`).
   *It is shown only once — keep it safe, it's like a password.*

### 3. Let Claude set it up
1. Open **Claude Code** in the `finradar-mcp` folder
   (in a terminal: `cd finradar-mcp` then `claude`; or open the folder from the Claude app).
2. Paste this message, with your token:
   > **Here is my FinRadar token: `frad_…` — please set everything up.**
3. Claude reads the included instructions, runs the bundled setup script (it stores your
   token securely, checks it against the live data, and connects the FinRadar tools), then
   greets you. If Claude asks you to **approve the "finradar" MCP server** or to reconnect
   (`/mcp`), say yes.

   *Prefer doing it yourself?* From the `finradar-mcp` folder, run one command —
   `python3 setup_finradar.py frad_YOUR_TOKEN` — and follow its output.

### 4. Start asking
Try, in your own words:
- *"Is **Colruyt Group** financially healthy? Explain it simply."*
- *"Find **IT companies** with solvency above 50% and at least €1M equity."*
- *"Who are the **directors and shareholders** of enterprise **0400378485**?"*
- *"Compare **equity and EBITDA** over the last 5 years for this company."*
- *"Show me companies near **Liège** in a difficult financial situation."*

Claude answers in **your language** (English, French or Dutch) and points you to the source.

---

## What it can do

- **Health check** of any Belgian company — solvency, liquidity, profit, multi-year trend,
  in plain words.
- **Find / screen companies** by sector, region and financial criteria (lead lists,
  benchmarks, distress lists).
- **Ownership & directors** — who controls a company, what a person or group owns.
- **People** — the companies an individual directs or owns (succession / key-person risk).

Every number comes from official sources; nothing is invented. On any company's FinRadar page
you can also export an Excel whose formulas reproduce the figures.

---

## Using Claude Desktop instead of Claude Code

Claude Desktop also supports MCP servers. Run `python3 setup_finradar.py frad_YOUR_TOKEN` once
(it stores your token and prints the exact launch command), then in Claude Desktop open
**Settings → Developer → Edit config** and add a `finradar` server using that command. If that
sounds fiddly, just use Claude Code — it's the smoother path. You can also paste the persona
from **`PERSONA.md`** into a Claude Project for the same tone.

---

## Privacy & safety

- Your token gives **read-only** access to public company data, **on behalf of your account**.
- It is stored **only on your computer** (`~/.finradar/token`), never inside this project,
  never shared. This repo is public — your token must never be committed.
- You can **revoke** a token at any time: FinRadar → profile → 🤖 AI agent → **Revoke**.
- Lost or leaked token? Revoke it and generate a new one.

---

## Troubleshooting

- **"Token rejected (401)"** → the token is wrong or was revoked. Generate a fresh one and
  tell Claude *"here is my new token: frad_…"*.
- **Tools don't appear** → reconnect: in Claude Code run `/mcp` (or reopen the folder), and
  approve the "finradar" server if asked.
- **"Python not found" (Windows)** → the `python3` that opens the Microsoft Store doesn't
  count. Install Python from <https://www.python.org/downloads/> and **tick "Add python.exe to
  PATH"**, then re-run `py -3 setup_finradar.py frad_YOUR_TOKEN`. (Claude can do this for you —
  just say *"I'm on Windows, set it up"*.)
- **Still stuck?** Tell Claude exactly what you see — it will diagnose and fix it. Everything
  the setup does lives in one script: `setup_finradar.py`.

---

## 🇫🇷 Démarrer en 4 étapes (~5 minutes)

Posez vos questions sur les entreprises belges **en langage naturel**, depuis votre propre
Claude : *« ACME est-elle en bonne santé financière ? »*, *« Trouve des sociétés de
construction rentables près de Liège »*, *« Qui contrôle cette entreprise ? »* — et obtenez
une réponse claire et **sourcée**, où chaque chiffre renvoie au dépôt officiel (KBO/BCE +
Banque nationale de Belgique).

**Ce qu'il vous faut :** un **compte FinRadar**, **Claude Code** (recommandé) ou Claude
Desktop, et 5 minutes. Aucune compétence technique.

**1. Récupérez le projet** — téléchargez le ZIP :
**[Télécharger finradar-mcp](https://github.com/vanbe/finradar-mcp/archive/refs/heads/main.zip)**
puis décompressez-le (dossier `finradar-mcp`). Ou, avec git :
`git clone https://github.com/vanbe/finradar-mcp.git`

**2. Générez votre token** — connectez-vous à FinRadar → votre **profil** (en haut à droite)
→ **🤖 Agent IA (token)** → **Générer un token** → **copiez-le** (il commence par `frad_`).
*Il n'est affiché qu'une seule fois — gardez-le comme un mot de passe.*

**3. Laissez Claude tout installer** — ouvrez **Claude Code** dans le dossier `finradar-mcp`,
puis collez ce message avec votre token :
> **Voici mon token FinRadar : `frad_…` — installe tout, s'il te plaît.**

Claude lit les instructions fournies, range votre token en lieu sûr, connecte les outils
FinRadar, fait un test rapide et vous accueille. S'il demande d'**autoriser le serveur MCP
« finradar »**, acceptez.

**4. Posez vos questions** (dans votre langue) :
- *« **Colruyt Group** est-elle solide financièrement ? Explique simplement. »*
- *« Trouve des **sociétés IT** avec une solvabilité > 50 % et au moins 1 M€ de fonds propres. »*
- *« Qui sont les **dirigeants et actionnaires** de l'entreprise **0400378485** ? »*
- *« Compare **fonds propres et EBITDA** sur 5 ans pour cette société. »*

**Confidentialité** — le token donne un accès **en lecture seule** aux données publiques, au
nom de votre compte ; il est stocké **uniquement sur votre ordinateur** (`~/.finradar/token`),
jamais dans ce dépôt public. Vous pouvez le **révoquer** à tout moment depuis votre profil.

**En cas de souci** — dites simplement à Claude ce que vous voyez (ex. « token refusé »,
« je ne vois pas les outils »), il diagnostique et corrige.
