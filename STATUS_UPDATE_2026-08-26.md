# Mapply — status correction, 2026-08-26

Replaces the "213 routes / 15 countries" figure in README.md, which is stale. This file is delivered as an addition, not merged into README.md in place, since the repo folder was set read-only for existing files this session.

## Real current state

**353 routes across 27 countries**, all tier-1 sourced where status is `published`.

The 15 countries in the original README are untouched at exactly 213 routes: UK (17), Germany (14), Netherlands (13), Portugal (15), Spain (15), France (15), Australia (15), Japan (15, +1 this session), Singapore (14), United States (14), Canada (16), UAE (14, +1 this session), Turkey (12), Switzerland (13), Ireland (13).

Twelve more countries were added at some point without a doc update, adding 140 routes: Brazil (11), China (11), Denmark (8), Italy (12, +1 this session), South Korea (15), Malaysia (11), Philippines (10), Poland (15), Russia (12), Saudi Arabia (13), Thailand (12), South Africa (11).

## What changed this session

- `my/de_rantau_pass.json` — upgraded draft → published (was tier-3 only, now tier-1: digital.gov.my, mdec.my)
- `za/remote_work_visa.json` — upgraded draft → published; **corrected a wrong income figure** (ZAR 650,976 → 650,796, per dha.gov.za)
- `th/dtv.json` — upgraded draft → published (was tier-3 only, now tier-1: mfa.go.th)
- `jp/digital_nomad_visa.json` — new route, added to repo
- `it/digital_nomad_visa.json` — new route, added to repo
- `ae/virtual_work_visa.json` — new route, added to repo

The three "upgraded" files are delivered separately as full replacement content, not written into the repo directly, per the same read-only rule — see the accompanying files and the chat message for what to paste where.

## Known gaps not yet closed

- National-variables files exist for only 12 of 27 countries (AU, BR, CH, DE, ES, FR, IE, IT, KR, PL, PT, TR) — may be fine if the other 15 simply have no formula-pegged thresholds, not independently confirmed.
- Full corpus-wide validation (`scripts/validate.py` against all 353+6 files, checking cross-references against the entire dataset) was not run this session — only the 6 new/changed files were validated in isolation against schema, tier-1 sourcing, and freshness rules. Run the real validator against the full repo before treating these as final.
