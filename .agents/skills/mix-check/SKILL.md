---
name: mix-check
description: Read mixer and device state and flag gain-staging, level, panning and masking risks. Read-only by default; changes only on my approval. Use when I say "mix-check", "check my mix", "why is this muddy" or before arranging/exporting.
---

# mix-check

A read-only health check of the mix, plus suggested fixes.

Follows `AGENTS.md`; never overrides its safety rules.

## Read

- Every track: name, volume (0–1 fader), pan, mute/solo, sends, device chain.
- Device parameters that matter (EQ bands, compressor threshold/ratio, utility
  gain) — read min / max / display values.
- Master: volume and devices.
- My habits in `music/production.md` → **Mix habits** (use them as the target).

## Report

Group findings, most important first:

1. **Gain staging** — faders pinned near max/min, master too hot, inconsistent
   levels between similar roles.
2. **Low end** — more than one track with heavy sub content, no high-pass on
   non-bass tracks, kick vs bass with no sidechain or EQ carve.
3. **Masking** — tracks sharing a role and register (from names, devices, clip
   pitch ranges).
4. **Stereo** — bass/kick panned off-center, everything dead center.
5. **Hygiene** — unnamed tracks, muted tracks with heavy devices, unused sends.

Note: agents can't hear the mix or read meters reliably — say which findings are
from settings vs inferred.

## Fix (only on approval)

Propose each fix with exact values (current → new, in display units). Apply only
the ones I approve, one undo batch each. Never touch the master chain without
asking.
