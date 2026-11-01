# 0002 — MCP server: mcp-server-ableton-live (wstierhout)

- Status: accepted, pending verification (plan step 4)
- Date: 2026-11-01

## Context

This PC ran `ahujasid/ableton-mcp` 1.4.5 via unpinned `uvx`. That package ships
a Supabase dataset recorder and telemetry module (`MCP_Server/dataset/`,
`telemetry.py`) and MCP tools that ask for dataset consent. It was disabled here
(`ABLETON_MCP_DISABLE_TELEMETRY=true`, consent `denied`), but the code path
exists and runs on every launch.

`mcp-server-ableton-live` (upstream `wstierhout/ableton-live-mcp`) was
recommended for undo/batch support, mixer tools, a doctor command, offline
`.als` tools and no telemetry in the server.

## Decision

Switch to `mcp-server-ableton-live`, pinned and hash-locked (see 0003).

Before installing, verify on PyPI/GitHub: latest release age (≥7 days), no
network calls beyond loopback, Windows support, Remote Script install path on
Windows, and compatibility with Live 12 Lite. Record results in
`docs/setup.md` Findings. If verification fails, reopen this decision.

## Consequences

- Replace the AbletonMCP Remote Script in
  `Documents/Ableton/User Library/Remote Scripts/` and reselect it in Live.
- `~/.ableton-mcp/consent.json` from the old server becomes unused.
