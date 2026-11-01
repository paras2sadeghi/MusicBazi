# MusicBazi

My personal Ableton Live production OS. This repo teaches AI agents my taste,
safety rules and workflow, and connects them to Live through one pinned
Ableton MCP server. Ableton stays the creative environment.

Works with **Claude Code**, **Cursor** and **Codex**, all running locally on this PC.

## Map

| Path | What |
|---|---|
| `AGENTS.md` | The agent contract — every agent reads this first |
| `CLAUDE.md` | Claude adapter (imports `AGENTS.md`) |
| `.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml` | Per-agent MCP config, all pointing at the same `.venv` server |
| `music/` | Taste library: identity, theory, genres, palette, production, references, taste-log |
| `tracks/<lane>/` | Journals per song or Machine set |
| `.agents/skills/` | Skills every agent can run (ideate, brainstorm, brain, reference-study, arrange, mix-check) |
| `scripts/` | `lock.py`, `setup.py`, `doctor.py` — run with `uv run` |
| `docs/` | Setup guide, Findings table, plan |
| `decisions/` | Why things are the way they are |

## Quick start

```bash
uv run scripts/setup.py
uv run scripts/doctor.py
```

Then in Live: Settings → Link, Tempo & MIDI → Control Surface → **AbletonMCP**,
Input/Output **None**. Full steps in `docs/setup.md`.
