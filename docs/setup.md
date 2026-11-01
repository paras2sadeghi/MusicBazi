# Setup

How this repo connects agents to Ableton Live, and how to keep it safe.

```text
agent (Claude Code / Cursor / Codex)
  └─ stdio → .venv/…/ableton-live-mcp  (mcp-server-ableton-live, pinned)
       └─ TCP 127.0.0.1:9877 → AbletonMCP Remote Script inside Live
            └─ the open Live Set
```

## Requirements

- Ableton Live 12 (this PC: **12.4.7 Lite**, Windows 11)
- [uv](https://docs.astral.sh/uv/) (this PC: 0.12.10; Python 3.14.7)

## Install

```bash
uv run --locked scripts/setup.py --install-remote-script
```

This builds `.venv` from `uv.lock` (hash-checked), links skills into
`.claude/skills/`, and installs the Remote Script to
`Documents\Ableton\User Library\Remote Scripts\AbletonMCP\` (Mac:
`~/Music/Ableton/User Library/…`). If a different AbletonMCP script is already
there, add `--replace`; the old one is backed up next to it as `__init__.py.*.bak`.

### Live Control Surface checklist

1. Quit Live completely, then reopen it.
2. **Settings → Link, Tempo & MIDI** (Live 12: *Tempo & MIDI → MIDI*).
3. In an empty **Control Surface** row choose **AbletonMCP**.
4. Set its **Input** and **Output** to **None**.
5. Make sure no other row uses an older Ableton MCP script (two bridges can't
   share port 9877).
6. Close Settings; dismiss any open Live dialog.
7. Run `uv run --locked scripts/doctor.py` — expect "Live bridge reachable".

## Agent configs

All three launch the same locked server with `uv run --locked ableton-live-mcp`
and the default toolsets below. The server name is `ableton` in each.

| Agent | File | First-use step |
|---|---|---|
| Claude Code | `.mcp.json` | Approve the `ableton` project server when prompted |
| Cursor | `.cursor/mcp.json` | Settings → MCP → enable `ableton` |
| Codex CLI / app | `.codex/config.toml` | Trust the project when Codex asks (untrusted projects ignore it) |

No global Ableton MCP config should exist (`~/.claude.json`, Claude Desktop,
`~/.cursor/mcp.json`, `~/.codex/config.toml`) — doctor warns if one does. The
old global `AbletonMCP` (ahujasid) entries were removed on 2026-11-01, and the
old Remote Script was backed up as `AbletonMCP\__init__.py.*.bak`.

**Watch out:** the old `ableton-mcp` (ahujasid) server copies its own Remote
Script over this one every time it starts. The Claude desktop app rewrote its
cached `AbletonMCP` entry back into `claude_desktop_config.json` once after
removal. If doctor warns about a global config, remove it in Claude →
Settings → Developer, then rerun doctor and check "Remote Script installed and
matches server".

## Health check

```bash
uv run --locked scripts/doctor.py           # full
uv run --locked scripts/doctor.py --offline # skip OSV query
```

The OSV query sends only package names and versions to api.osv.dev — no Live data.

## Upgrading the server

1. Read the new version's changelog and **re-read its code for network calls,
   telemetry or consent prompts** (decisions/0002).
2. Change the pin in `pyproject.toml`.
3. `uv run scripts/lock.py` — applies the 7-day minimum release age.
4. `uv run --locked scripts/setup.py --install-remote-script --replace`
5. Restart Live, reselect AbletonMCP, run doctor.
6. Commit `pyproject.toml` + `uv.lock` with the review notes.

## Toolsets

The server loads all tool groups unless `ABLETON_TOOLSETS` is set. Agent configs
use:

```text
session,tracks,clips,devices,browser,arrangement,generators,analysis
```

Left out on purpose: `audio` and `offline` (read arbitrary files on disk —
AGENTS.md safety 7) and `recipes`. Add a group for a task when needed.

## Server audit — mcp-server-ableton-live 1.8.1 (2026-11-01)

Wheel downloaded from PyPI and read before install.

| Check | Result |
|---|---|
| Release date | 2026-09-17 (45 days before lock — passes 7-day rule) |
| License | MIT |
| Outbound network | None. Only socket use is the client connecting to `ABLETON_HOST` (default `localhost`) port 9877 |
| Remote Script bind | `127.0.0.1:9877` by default; no auth, so never set `ABLETON_MCP_HOST` to a public address |
| Telemetry / analytics / consent | None found (no HTTP clients, no Supabase, no consent tools) |
| File access | `audio`, `audio_analysis` and `offline` tools read paths passed to them; excluded from default toolsets |
| Windows support | Yes — installer targets `Documents\Ableton\User Library`; refuses symlinked targets; backs up before `--replace` |
| Env vars | `ABLETON_HOST`, `ABLETON_PORT`, `ABLETON_TOOLSETS`, `ABLETON_LOG_LEVEL`, `ABLETON_USER_LIBRARY`; Remote Script: `ABLETON_MCP_HOST`, `ABLETON_MCP_PORT` |
| Dependency vulns | 0 known in 40 locked packages (OSV, 2026-11-01) |

Compared with the previous server (`ahujasid/ableton-mcp` 1.4.5): that package
bundled a Supabase dataset recorder and telemetry module, gated by consent.

## Findings

Behaviour of individual tools in Live — filled during validation (plan step 7).

| Operation | Verdict | Notes |
|---|---|---|
| <!-- fill during validation --> | | |
