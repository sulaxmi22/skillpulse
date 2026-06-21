# SkillPulse — Skill Death Clock

> Real-time skill market agent: is your skill growing, dying, or transforming?


https://github.com/user-attachments/assets/6b967093-741b-4fcd-b5a6-95d93d3610cd


## Quick Start

### 1. Add your API key
Open `.env` and paste your Anthropic key:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

### 2. Run the server
```bash
python server.py
```

### 3. Open in browser
```
http://localhost:3000
```

---

## Project Structure

```
skillpulse/
├── .env              ← API keys go here (never commit)
├── .gitignore        ← protects .env from git
├── server.py         ← local dev server, injects keys from .env
├── README.md
└── public/
    └── index.html    ← full app (UI + Claude API calls)
```

---

## How it works

1. User enters a skill (e.g. "React", "Excel VBA", "LangChain")
2. App calls Claude API with built-in **web search tool**
3. Claude searches live job postings, GitHub, industry signals
4. Returns structured JSON verdict
5. UI renders: verdict, demand score, replacement skills, upgrade path, live evidence

## Output per skill

| Field | Description |
|---|---|
| Verdict | Growing / Stable / Declining / Transforming / Dying |
| Demand Score | 0–100 based on job posting volume |
| Confidence | 0–100 based on number of sources found |
| Risk Level | Low / Medium / High |
| Replacement Skills | What's taking over |
| Upgrade Path | What to learn next |
| Live Evidence | Real job post snippets with source + date |

---

## API Keys

| Key | Where to get |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys |
| `BRIGHT_DATA_TOKEN` | brightdata.com/cp/setting → API tokens |
