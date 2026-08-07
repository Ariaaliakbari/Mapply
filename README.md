# Mapply

A free, public, structured directory of legal immigration and relocation routes worldwide — visas, work permits, ancestry routes, study routes, business/investment routes, family routes, humanitarian routes, and settlement/citizenship routes.

**Never charged to individual applicants. Ever.** That's a permanent line, not a launch promise.

## What makes this different

Every other source in this space is one of:
- a single-country government site (accurate, but can't be compared to anywhere else)
- a law-firm eligibility checker (lead-gen, single-country)
- an SEO content farm (articles, not structured data, often stale)

Mapply is the only place building one shared schema across every country, so a route in Norway and a route in Turkey are the same shape and directly comparable.

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every **hard** (disqualifying) requirement must cite a **tier-1 source** — meaning an actual government publication, not a law firm or blog
- Every route carries a `verified_at` date. Data older than 180 days automatically fails validation; past 90 days it's flagged with a warning
- `scripts/validate.py` runs automatically (via GitHub Actions, see `.github/workflows/validate.yml`) on every change, checking schema compliance, source tiering, and cross-references between routes

## Status

Early. One route encoded (`routes/uk/skilled_worker.json`) as a working proof of the schema. Everything else is next.

## Contributing

See `CONTRIBUTING.md`. Short version: any change to a threshold value needs a real tier-1 source link, or it won't pass CI.
