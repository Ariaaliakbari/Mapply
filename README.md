**Never charged to individual applicants. Ever.** That is a permanent line.

## What makes this different

Every other source is one of the following things listed here.

Mapply is the only place building one shared schema across every country, so a route in the UK and a route in Japan are the same shape and directly comparable.

## Status

**356 routes live across 27 countries, all 9 categories, all published routes tier-1 (government-only) sourced.**

- **UK**: 17 routes
- **Germany**: 14 routes
- **Netherlands**: 13 routes
- **Portugal**: 15 routes
- **Spain**: 15 routes
- **France**: 15 routes
- **Australia**: 15 routes
- **Japan**: 15 routes
- **Singapore**: 14 routes
- **United States**: 14 routes
- **Canada**: 16 routes
- **UAE**: 14 routes
- **Turkey**: 12 routes
- **Switzerland**: 13 routes
- **Ireland**: 13 routes
- **Brazil**: 11 routes
- **China**: 11 routes
- **Denmark**: 8 routes
- **Italy**: 12 routes
- **South Korea**: 15 routes
- **Malaysia**: 11 routes
- **Philippines**: 10 routes
- **Poland**: 15 routes
- **Russia**: 12 routes
- **Saudi Arabia**: 13 routes
- **Thailand**: 12 routes
- **South Africa**: 11 routes

Multiple live stale-data catches confirmed against tier-1 sources during encoding (see route notes fields) — most recently a wrong South African income threshold (ZAR 650,976 vs the correct 650,796) caught 2026-08-26.

Some `draft`-status routes may still cite tier-3 (non-government) sources only; `published` routes are always tier-1, enforced by CI.

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every hard (disqualifying) requirement on a `published` route must cite a tier-1 source, not a law firm or blog. Enforced by CI.
- Every route carries a verified_at date. Data older than 180 days fails validation; past 90 days it is flagged.
- Formula-valued requirements reference `national-variables/<country>.json` instead of hardcoding a number that goes stale every January. CI checks it matches. (Currently populated for 12 of 27 countries — AU, BR, CH, DE, ES, FR, IE, IT, KR, PL, PT, TR.)
- Group-level overrides let one route express different outcomes for different qualifying paths without splitting a single government-named route into fake ones.
- Closed routes stay in the dataset with status closed and a superseded_by pointer (or null if there is no successor), rather than disappearing.
- status draft covers incomplete sourcing, or a route enacted in law but not yet operationally available.
- scripts/validate.py runs automatically via GitHub Actions on every change.

## Repo structure

- schema/route.schema.json - the route shape every file must follow
- `routes/<country-code>/*.json` - 27 countries: uk, de, nl, pt, es, fr, au, jp, sg, us, ca, ae, tr, ch, ie, br, cn, dk, it, kr, my, ph, pl, ru, sa, th, za
- `national-variables/<COUNTRY>.json` - reference values formula-based requirements peg to
- scripts/validate.py - CI validator

## Contributing
See CONTRIBUTING.md. Short version: any change to a threshold value needs a real tier-1 source link, or it will not pass CI.
