# 0005 — Agents may generate full drafts

- Status: accepted
- Date: 2026-11-01

## Context

The source prompt limits agents to a production assistant role: no whole songs,
no adding tracks or loading instruments. I want agents to be able to generate
full drafts I can react to.

## Decision

Agents may generate sections or whole songs, add tracks (within Live Lite's 16
track limit) and load Vital or Live stock devices, when I ask or a skill I
invoked calls for it. All safety rules in `AGENTS.md` still apply: duplicated
`.als` first, ask before destructive edits, read → say → write, one idea per
undo batch, no telemetry, no disk browsing.

## Consequences

- Generated material must follow `music/` taste files; gaps are flagged, not filled
  with invented taste.
- Output is framed as a draft for reaction, feeding the ideate → taste-log loop.
