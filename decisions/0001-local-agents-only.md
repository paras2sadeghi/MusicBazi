# 0001 — Local agents only: Claude Code, Cursor, Codex

- Status: accepted
- Date: 2026-11-01

## Context

I want any agent to be able to drive Ableton from this repo. The Ableton
Remote Script listens on `127.0.0.1:9877` (loopback only). Claude Code, Cursor
and Codex all launch local stdio MCP servers. The ChatGPT desktop/web app only
connects to remote HTTPS MCP servers, which would mean exposing my Live session
through a public tunnel.

## Decision

Support Claude Code, Cursor and Codex (CLI/app), each with a thin project-scoped
config (`.mcp.json`, `.cursor/mcp.json`, `.codex/config.toml`) that launches the
same server from this repo's `.venv`. `AGENTS.md` is the single source of rules.
The ChatGPT app is out of scope.

## Consequences

- Ableton tools load only inside this repo, always alongside `AGENTS.md`.
- The global `AbletonMCP` entries in `~/.claude.json` and Claude Desktop config
  get removed (with confirmation) when the project configs land.
- Revisit if a ChatGPT app gains local stdio MCP support.
