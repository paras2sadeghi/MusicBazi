# 0004 — Scripts in Python, run via `uv run`

- Status: accepted
- Date: 2026-11-01

## Context

The source prompt uses bash scripts and symlinks for a Mac. This repo lives on
Windows 11 and should stay usable from a Mac and from any of the three agents.

## Decision

Write `scripts/lock.py`, `scripts/setup.py` and `scripts/doctor.py` in Python
and run them with `uv run`. `setup.py` also creates the `.claude/skills/` links
to `.agents/skills/` (directory junctions on Windows, symlinks elsewhere).

## Consequences

- One implementation for every OS; doctor and audit share code.
- `.claude/skills/` is git-ignored and recreated by `setup.py` after a clone.
