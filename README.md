**Never charged to individual applicants. Ever.** That is a permanent line.

## What makes this different

Every other source is one of the following things listed here.

Mapply is the only place building one shared schema across every country, so a route in the UK and a route in Japan are the same shape and directly comparable.

## Status

**213 routes live across 15 countries, all 9 categories, all tier-1 (government-only) sourced.**

- **UK**: 17 routes
- **Germany**: 14 routes
- **Netherlands**: 13 routes
- **Portugal**: 15 routes
- **Spain**: 15 routes
- **France**: 15 routes
- **Australia**: 15 routes
- **Japan**: 14 routes
- **Singapore**: 14 routes
- **United States**: 14 routes
- **Canada**: 16 routes
- **UAE**: 13 routes
- **Turkey**: 12 routes
- **Ireland**: 13 routes

Multiple live stale-data catches confirmed against tier-1 sources during encoding (see route notes fields).

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every hard (disqualifying) requirement must cite a tier-1 source, not a law firm or blog. Enforced by CI.
- Every route carries a verified_at date. Data older than 180 days fails validation; past 90 days it is flagged.
- Formula-valued requirements reference `national-variables/<country>.json` instead of hardcoding a number that goes stale every January. CI checks it matches.
- Group-level overrides let one route express different outcomes for different qualifying paths without splitting a single government-named route into fake ones.
- Closed routes stay in the dataset with status closed and a superseded_by pointer (or null if there is no successor), rather than disappearing.
- status draft covers incomplete sourcing, or a route enacted in law but not yet operationally available.
- scripts/validate.py runs automatically via GitHub Actions on every change.

## Repo structure

- schema/route.schema.json - the route shape every file must follow
- `routes/<country-code>/*.json` - e.g. uk, de, nl, pt, es, fr, au, jp, sg, us, ca, ae, tr, ch, ie
- `national-variables/<COUNTRY>.json` - reference values formula-based requirements peg to
- scripts/validate.py - CI validator

## Contributing
See CONTRIBUTING.md. Short version: any change to a threshold value needs a real tier-1 source link, or it will not pass CI.
