# MusicBazi — implementation plan

Personal Ableton Live production OS: a repo that teaches any local agent
(Claude Code, Cursor, Codex) my taste, safety rules and workflow, and wires all
of them to the same pinned Ableton MCP server.

Source: a friend's setup prompt (`friend-ableton-mcp-setup-prompt.md`), reviewed
against this PC on 2026-11-01. Decisions below come from that review + interview.

## Current state (before)

| Item | Found | Gap vs. target |
|---|---|---|
| Repo | Empty, `origin` → github.com/paras2sadeghi/MusicBazi, branch `main` | Everything to scaffold |
| Live | **Live 12 Lite** (12.4.6), Windows 11 | Prompt assumes Mac + Suite |
| MCP server | `ahujasid/ableton-mcp` 1.4.5 via unpinned `uvx` | Replace with wstierhout; pin + lock |
| MCP config | Global: `~/.claude.json` + Claude Desktop config | Move to project-scoped, per-tool adapters |
| Data collection | Server ships Supabase dataset uploader; telemetry env-disabled, consent `denied` in `~/.ableton-mcp/consent.json` | Gone after switch; keep refusal rule in AGENTS.md |
| Remote Script | `Documents/Ableton/User Library/Remote Scripts/AbletonMCP` (ahujasid) | Replace with wstierhout's script |
| Plugins | Vital, Splice | Record in `music/palette.md` |

## Decisions

| # | Topic | Choice | Departs from prompt? |
|---|---|---|---|
| D1 | Agents | Claude Code, Cursor, Codex CLI/app — all local stdio | ChatGPT app excluded (needs public tunnel) |
| D2 | Server | Switch to `mcp-server-ableton-live` (wstierhout) | No |
| D3 | Lock | `uv` lockfile with hashes + `exclude-newer` 7-day window | Tool differs (uv vs pip), same guarantees |
| D4 | Scripts | Python run via `uv run` (cross-platform) | Yes — no `.sh` on Windows |
| D5 | Edition | Respect Lite limits (16 tracks, 8 scenes, Lite devices); list upgrade wants | Prompt didn't cover |
| D6 | Agent role | **Full generator** — may build whole drafts, add tracks, load Vital/stock devices | **Yes** — prompt says assistant only. Safety rules still apply |
| D7 | Skills | ideate, brainstorm, brain, reference-study, arrange, mix-check | Adds 3 |
| D8 | Taste build | Interview now (below) + grow via ideate | No |
| D9 | Learning | Agents propose principles; I confirm before they're saved | No |
| D10 | Git | Commit per step on `main`; push only when asked | No |

Each of D1–D4 and D6 gets an ADR in `decisions/`.

## Taste seed (deep interview, 2026-11-01 — replaces first draft)

- **North star:** ethereal, dark electronic with 90s soul — emotional *and* danceable; layered but minimal.
- **Feeling:** melancholic-but-hopeful + dark / hypnotic.
- **Lanes:** `techno` (driving peak-time + hypnotic), `darkwave-techno`, `darkwave`, `triphop-dark-alt`.
  Persian fusion, lo-fi and pop dropped.
- **Scales:** Hirajoshi for hooks/arps; harmony per lane (static in techno, minor progressions in darkwave/trip-hop).
- **Sounds:** cold FM/digital, M1-era romplers, acid mono bass; big reverbs/delays, 80s chorus/flanger, grit.
- **Drums:** drum machines, gated 80s snares, slow dusty breaks.
- **Density:** ≤ 3 focal parts + quiet textures.
- **Hooks:** evolve via automation; tension notes.
- **Vocals:** song first; vocal melodies + space only when asked.
- **Pain points:** loops never become songs, boring melodies, cheap sounds.
- **References:** see `music/reference-artists.md` (HNGT and IVOXIGEN to confirm).

## Target layout

```text
MusicBazi/
  AGENTS.md                 # sole agent contract (Codex + Cursor read natively)
  CLAUDE.md                 # only: @AGENTS.md
  README.md
  .mcp.json                 # Claude Code → .venv server
  .cursor/mcp.json          # Cursor → same server
  .codex/config.toml        # Codex → same server
  pyproject.toml, uv.lock   # pinned server + hash lock
  scripts/
    lock.py                 # uv lock with 7-day exclude-newer
    setup.py                # uv sync --locked; install Remote Script; link skills
    doctor.py               # lock/audit (OSV), port 9877 bridge, Remote Script version, Lite check
  docs/setup.md             # install, Control Surface checklist, Findings table
  decisions/                # ADRs
  music/  identity theory genres palette production reference-artists taste-log
  tracks/<lane>/<song>.md
  .agents/skills/<skill>/SKILL.md     # single source of skills
  .claude/skills/<skill>    # junctions → .agents/skills (Windows: no admin needed)
```

## AGENTS.md contract — adjustments for D6 (full generator)

Keep the prompt's safety rules; loosen only the creation scope:
- May generate full drafts, add tracks (≤16 total, Lite), load Vital / stock devices.
- Always on a **duplicated `.als`** — confirm before the first write in a session.
- Ask before destructive edits (delete track/device/clip, replace all notes, overwrite arrangement).
- Read state → state the plan → write; one musical idea = one undo batch.
- Read before writing notes: identity, theory, lane in genres, taste-log category, track journal, live clip pitch classes.
- Never accept telemetry/consent prompts; no disk browsing outside paths I name; export/freeze stay manual.
- 0-based tool indices vs my 1-based speech; name the track back.

## Implementation order

1. Scaffold: `.gitignore`, README, AGENTS.md, CLAUDE.md, ADRs. *(commit)*
2. `music/` files with taste seed + `<!-- fill -->`; `tracks/` lanes. *(commit)*
3. Six skills in `.agents/skills/` + Claude junctions. *(commit)*
4. Verify wstierhout package on PyPI (release age, data collection, Windows support, Remote Script install path); `pyproject.toml`, `lock.py`, `setup.py`, `doctor.py`; build `.venv`. *(commit)*
5. Swap Remote Script; write `.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml`; remove global AbletonMCP entries from `~/.claude.json` and Claude Desktop config (confirm first). *(commit)*
6. Walk through Live Control Surface setup; run doctor with Live open.
7. Validate on a throwaway set from each agent: read state → small MIDI write → undo → Findings table in `docs/setup.md`. *(commit)*

## Open risks

- wstierhout package details (Windows support, Lite compatibility, toolset names) are not yet verified — step 4 checks before anything is installed.
- Lite device limits may block some generator tools; doctor should report which.
- Junctions for `.claude/skills` don't survive a git clone on another OS; `setup.py` recreates them.
