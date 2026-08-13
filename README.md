# Mapply

A free, public, structured directory of legal immigration and relocation routes worldwide — visas, work permits, ancestry routes, study routes, business/investment routes, family routes, humanitarian routes, and settlement/citizenship routes.

**Never charged to individual applicants. Ever.** That's a permanent line, not a launch promise.

## What makes this different

Every other source in this space is one of:
- a single-country government site (accurate, but can't be compared to anywhere else)
- a law-firm eligibility checker (lead-gen, single-country)
- an SEO content farm (articles, not structured data, often stale)

Mapply is the only place building one shared schema across every country, so a route in the UK and a route in Germany are the same shape and directly comparable.

## Status

**31 routes live across 2 countries, all 9 categories, all tier-1 (government-only) sourced.**

- **UK**: 17 routes — Skilled Worker, ILR, Global Talent, Student, Graduate, Citizenship, Innovator Founder, Family/Spouse, High Potential Individual, Health & Care Worker, Youth Mobility, UK Ancestry, Scale-up, Standard Visitor, BNO, Asylum, Start-up (closed, superseded by Innovator Founder)
- **Germany**: 14 routes — EU Blue Card, Chancenkarte, Job Seeker (post-study), Freelance/Self-employment, ICT Card, Family Reunification, §116(2) Citizenship Restoration, Naturalisation, Settlement permit (Niederlassungserlaubnis), Student, Ausbildung, Asylum, EU Family Member, Schengen Visitor

Multiple live stale-data catches confirmed against tier-1 sources during encoding (see individual route `notes` fields) — this is the core, empirically-proven thesis of the whole project, not a hypothetical.

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every **hard** (disqualifying) requirement must cite a **tier-1 source** — an actual government publication, not a law firm or blog. Enforced by CI, not just policy.
- Every route carries a `verified_at` date. Data older than 180 days automatically fails validation; past 90 days it's flagged with a warning
- **Formula-valued requirements** (e.g. Germany's Blue Card salary, pegged to a percentage of the pension contribution ceiling) reference `national-variables/<country>.json` instead of hardcoding a number that goes stale every January. CI checks the displayed figure actually matches the formula.
- **Group-level overrides** (`outcome_override`, `prerequisites_override`) let a single route express different outcomes for different qualifying paths — e.g. UK Global Talent's Exceptional Talent vs Exceptional Promise tiers, or Germany's settlement timeline varying by feeder route — without splitting one government-named route into several fake ones.
- **Closed routes stay in the dataset** with `status: "closed"` and a `superseded_by` pointer, rather than disappearing — someone searching for a route that no longer exists should find it, with a clear pointer to what replaced it.
- `scripts/validate.py` runs automatically via GitHub Actions on every change, checking schema compliance, source tiering, formula consistency, closed-route completeness, and cross-references between routes.

## Repo structure

```
schema/
  route.schema.json           the route shape every file must follow
  national_variable.schema.json
routes/
  uk/*.json
  de/*.json
national-variables/
  DE.json                     reference values formula-based requirements peg to
scripts/
  validate.py                 CI validator
```

## Contributing

See `CONTRIBUTING.md`. Short version: any change to a threshold value needs a real tier-1 source link, or it won't pass CI.
