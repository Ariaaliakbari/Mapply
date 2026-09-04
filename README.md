**Never charged to individual applicants. Ever.** That is a permanent line.

## What makes this different

Every other source is one of the following things listed here.

Mapply is the only place building one shared schema across every country, so a route in the UK and a route in Japan are the same shape and directly comparable.

## Status

**896 routes live across 77 countries, all 9 categories, all published routes tier-1 (government-only) sourced.**

- **United Kingdom**: 17 · **Canada**: 16 · **Australia**: 15 · **France**: 15 · **Japan**: 15 · **Poland**: 15 · **Portugal**: 15 · **South Korea**: 15 · **Spain**: 15 · **UAE**: 15
- **Austria**: 14 · **Georgia**: 14 · **Germany**: 14 · **Hungary**: 14 · **Singapore**: 14 · **United States**: 14
- **Costa Rica**: 13 · **Cyprus**: 13 · **Dominican Republic**: 13 · **Greece**: 13 · **Ireland**: 13 · **Netherlands**: 13 · **Saudi Arabia**: 13 · **Serbia**: 13 · **Switzerland**: 13
- **Bahamas**: 12 · **Bulgaria**: 12 · **Croatia**: 12 · **Czechia**: 12 · **Ecuador**: 12 · **Italy**: 12 · **Luxembourg**: 12 · **Malta**: 12 · **Mexico**: 12 · **New Zealand**: 12 · **Russia**: 12 · **Thailand**: 12 · **Turkey**: 12
- **Argentina**: 11 · **Brazil**: 11 · **Cayman Islands**: 11 · **China**: 11 · **Colombia**: 11 · **Finland**: 11 · **Grenada**: 11 · **Malaysia**: 11 · **Morocco**: 11 · **Norway**: 11 · **South Africa**: 11 · **Turks and Caicos**: 11
- **Albania**: 10 · **Antigua and Barbuda**: 10 · **Aruba**: 10 · **Barbados**: 10 · **Belgium**: 10 · **Bermuda**: 10 · **Curaçao**: 10 · **Estonia**: 10 · **Iceland**: 10 · **Indonesia**: 10 · **Oman**: 10 · **Philippines**: 10 · **Trinidad and Tobago**: 10 · **Uruguay**: 10
- **Anguilla**: 9 · **Belarus**: 9 · **British Virgin Islands**: 9 · **Dominica**: 9 · **Montserrat**: 9 · **Panama**: 9 · **Saint Kitts and Nevis**: 9 · **Saint Lucia**: 9 · **Sint Maarten**: 9 · **Sweden**: 9
- **Denmark**: 8 · **Egypt**: 8 · **Saint Vincent and the Grenadines**: 8

Counts generated directly from `routes/<code>/*.json` file counts, not hand-maintained — verify against the repo if this drifts again.

Multiple live stale-data catches confirmed against tier-1 sources during encoding (see route notes fields) — most recently a wrong South African income threshold (ZAR 650,976 vs the correct 650,796) caught 2026-08-26.

**Note on the 2026-08-26/08-28 expansion:** 50 countries and ~500 routes were added across two sessions without per-country "notable findings during encoding" documentation — unlike the original 15-27 country build. No fabricated narrative has been added here to paper over that gap. Anyone relying on this data should treat these countries as encoded-but-not-narratively-audited until a real review pass happens.

Some `draft`-status routes may still cite tier-3 (non-government) sources only; `published` routes are always tier-1, enforced by CI.

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every hard (disqualifying) requirement on a `published` route must cite a tier-1 source, not a law firm or blog. Enforced by CI.
- Every route carries a verified_at date. Data older than 180 days fails validation; past 90 days it is flagged.
- Formula-valued requirements reference `national-variables/<country>.json` instead of hardcoding a number that goes stale every January. CI checks it matches. (Currently populated for 12 of 77 countries — AU, BR, CH, DE, ES, FR, IE, IT, KR, PL, PT, TR. Not confirmed whether the other 65 have no formula-pegged thresholds or are just missing coverage.)
- Group-level overrides let one route express different outcomes for different qualifying paths without splitting a single government-named route into fake ones.
- Closed routes stay in the dataset with status closed and a superseded_by pointer (or null if there is no successor), rather than disappearing.
- status draft covers incomplete sourcing, or a route enacted in law but not yet operationally available.
- scripts/validate.py runs automatically via GitHub Actions on every change.

## Repo structure

- schema/route.schema.json - the route shape every file must follow
- `routes/<country-code>/*.json` - 77 countries: ae, ag, ai, al, ar, at, au, aw, bb, be, bg, bm, br, bs, by, ca, ch, cn, co, cr, cw, cy, cz, de, dk, dm, do, ec, ee, eg, es, fi, fr, gd, ge, gr, hr, hu, id, ie, is, it, jp, kn, kr, ky, lc, lu, ma, ms, mt, mx, my, nl, no, nz, om, pa, ph, pl, pt, rs, ru, sa, se, sg, sx, tc, th, tr, tt, uk, us, uy, vc, vg, za
- `national-variables/<COUNTRY>.json` - reference values formula-based requirements peg to
- scripts/validate.py - CI validator

## Contributing
See CONTRIBUTING.md. Short version: any change to a threshold value needs a real tier-1 source link, or it will not pass CI.
