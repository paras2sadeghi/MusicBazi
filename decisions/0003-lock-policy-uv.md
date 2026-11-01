# 0003 — Dependency lock: uv lockfile, hashes, 7-day release age

- Status: accepted
- Date: 2026-11-01

## Context

The MCP server runs with access to my Live session and can reach the network.
An unpinned `uvx` launch picks up whatever was published last, including a
compromised release. The source prompt asked for pip `--require-hashes` plus a
minimum release age of 7 days.

## Decision

Use `uv` instead of pip:

- `pyproject.toml` pins `mcp-server-ableton-live` to an exact version.
- `scripts/lock.py` runs `uv lock` with `--exclude-newer` set to 7 days ago, so
  no package in the tree is newer than a week. `uv.lock` records hashes.
- `scripts/setup.py` builds `.venv` with `uv sync --locked` only.
- Lowering the 7-day window needs a dated exception in this file that I approve.

## Consequences

- Same guarantees as the pip approach, native on Windows and Mac.
- Upgrades are deliberate: re-read the server code for data collection, re-lock,
  run doctor, commit.
