**Never charged to individual applicants. Ever.** That is a permanent line.

## What makes this different

Every other source is one of the following things listed here.

Mapply is the only place building one shared schema across every country, so a route in the UK and a route in Japan are the same shape and directly comparable.

## Status

**1,560 routes live across 148 countries, all 9 categories.** 932 are `published` (tier-1/government sourced, enforced by CI). 615 are `draft` — structurally complete but not yet fully tier-1 sourced, not shown publicly. 13 are `closed`.

- **United Kingdom**: 17
- **Canada**: 16
- **Australia**: 15 · **France**: 15 · **Japan**: 15 · **Poland**: 15 · **Portugal**: 15 · **South Korea**: 15 · **Spain**: 15 · **UAE**: 15
- **Austria**: 14 · **Georgia**: 14 · **Germany**: 14 · **Hungary**: 14 · **Lithuania**: 14 · **Moldova**: 14 · **Singapore**: 14 · **United States**: 14
- **Costa Rica**: 13 · **Cyprus**: 13 · **Dominican Republic**: 13 · **Ethiopia**: 13 · **Greece**: 13 · **Ireland**: 13 · **Jamaica**: 13 · **Netherlands**: 13 · **Nigeria**: 13 · **Saudi Arabia**: 13 · **Serbia**: 13 · **Switzerland**: 13
- **Armenia**: 12 · **Bahamas**: 12 · **Bulgaria**: 12 · **Croatia**: 12 · **Czechia**: 12 · **Ecuador**: 12 · **Fiji**: 12 · **Italy**: 12 · **Luxembourg**: 12 · **Malta**: 12 · **Mexico**: 12 · **New Zealand**: 12 · **Peru**: 12 · **Qatar**: 12 · **Russia**: 12 · **Slovakia**: 12 · **Thailand**: 12 · **Turkey**: 12
- **Argentina**: 11 · **Bahrain**: 11 · **Botswana**: 11 · **Brazil**: 11 · **Cayman Islands**: 11 · **Chile**: 11 · **China**: 11 · **Colombia**: 11 · **Côte d'Ivoire**: 11 · **Finland**: 11 · **Grenada**: 11 · **Israel**: 11 · **Jordan**: 11 · **Malaysia**: 11 · **Morocco**: 11 · **Norway**: 11 · **Romania**: 11 · **Rwanda**: 11 · **South Africa**: 11 · **Turks and Caicos**: 11 · **Uganda**: 11 · **Ukraine**: 11 · **Vietnam**: 11
- **Albania**: 10 · **Antigua and Barbuda**: 10 · **Aruba**: 10 · **Bangladesh**: 10 · **Barbados**: 10 · **Belgium**: 10 · **Bermuda**: 10 · **Chad**: 10 · **Curaçao**: 10 · **Estonia**: 10 · **Ghana**: 10 · **Iceland**: 10 · **Indonesia**: 10 · **Kenya**: 10 · **Latvia**: 10 · **Mongolia**: 10 · **Oman**: 10 · **Pakistan**: 10 · **Paraguay**: 10 · **Philippines**: 10 · **Sri Lanka**: 10 · **Trinidad and Tobago**: 10 · **Uruguay**: 10
- **Anguilla**: 9 · **Azerbaijan**: 9 · **Belarus**: 9 · **Bolivia**: 9 · **British Virgin Islands**: 9 · **Dominica**: 9 · **Kazakhstan**: 9 · **Lebanon**: 9 · **Montenegro**: 9 · **Montserrat**: 9 · **Panama**: 9 · **Saint Kitts and Nevis**: 9 · **Saint Lucia**: 9 · **Senegal**: 9 · **Sint Maarten**: 9 · **Sweden**: 9 · **Syria**: 9 · **Tanzania**: 9
- **Algeria**: 8 · **Angola**: 8 · **Bosnia and Herzegovina**: 8 · **Burkina Faso**: 8 · **Cameroon**: 8 · **Cuba**: 8 · **DR Congo**: 8 · **Denmark**: 8 · **Egypt**: 8 · **El Salvador**: 8 · **Guatemala**: 8 · **Haiti**: 8 · **Honduras**: 8 · **India**: 8 · **Iraq**: 8 · **Kosovo**: 8 · **Kyrgyzstan**: 8 · **Libya**: 8 · **Mali**: 8 · **Mozambique**: 8 · **Nicaragua**: 8 · **Niger**: 8 · **North Macedonia**: 8 · **Republic of the Congo**: 8 · **Saint Vincent and the Grenadines**: 8 · **Slovenia**: 8 · **Uzbekistan**: 8 · **Venezuela**: 8 · **Zimbabwe**: 8
- **Iran**: 7 · **Myanmar**: 7 · **Somalia**: 7 · **Sudan**: 7
- **Afghanistan**: 6 · **Kuwait**: 6 · **Tunisia**: 6

Counts generated directly from `routes/<code>/*.json` file counts, not hand-maintained — verify against the repo if this drifts again.

Multiple live stale-data catches confirmed against tier-1 sources during encoding (see route notes fields) — most recently a wrong South African income threshold (ZAR 650,976 vs the correct 650,796) caught 2026-08-26.

**Note on undocumented expansion, updated 2026-09-09:** as of the last README pass (2026-08-26/08-28/09-04/09-06), the repo had grown to 138 countries / 1,479 routes without per-country research notes for the newest ones (Algeria through Zimbabwe — see git history for that list). Since then, 10 more countries and 81 more routes were added — Afghanistan, Angola, Bolivia, Cameroon, Iraq, Kyrgyzstan, Libya, Mozambique, Paraguay, Republic of the Congo — again with zero note in this file or a status update. Of those 81 routes, 10 are already `published` with tier-1 sources (they pass CI's tier-1 enforcement, not just self-declared); 71 are still `draft`. This file has now been resynced against the real repo three times for the same reason. This is the recurring failure mode named in the project brief: data work keeps outrunning the point where docs and UI work were supposed to happen instead. No per-country "notable findings" narrative exists for these 10 countries, on top of the ones already flagged from the prior gaps. Treat them as encoded-but-not-narratively-audited until a real review pass happens.

Some `draft`-status routes may still cite tier-3 (non-government) sources only; `published` routes are always tier-1, enforced by CI.

## How the data works

- Every route lives as one JSON file under `routes/<country>/`, following `schema/route.schema.json`
- Every hard (disqualifying) requirement on a `published` route must cite a tier-1 source, not a law firm or blog. Enforced by CI.
- Every route carries a verified_at date. Data older than 180 days fails validation; past 90 days it is flagged.
- Formula-valued requirements reference `national-variables/<country>.json` instead of hardcoding a number that goes stale every January. CI checks it matches. (Currently populated for 14 of 148 countries — AU, BR, CH, DE, ES, FR, IE, IT, KR, LT, PE, PL, PT, TR. Not confirmed whether the other 134 have no formula-pegged thresholds or are just missing coverage — that gap has not been re-checked against the 10 countries added since the last README pass.)
- Group-level overrides let one route express different outcomes for different qualifying paths without splitting a single government-named route into fake ones.
- Closed routes stay in the dataset with status closed and a superseded_by pointer (or null if there is no successor), rather than disappearing.
- status draft covers incomplete sourcing, or a route enacted in law but not yet operationally available.
- scripts/validate.py runs automatically via GitHub Actions on every change.

## Repo structure

- `schema/route.schema.json` - the route shape every file must follow
- `routes/<country-code>/*.json` - 148 countries: ae, af, ag, ai, al, am, ao, ar, at, au, aw, az, ba, bb, bd, be, bf, bg, bh, bm, bo, br, bs, bw, by, ca, cd, cg, ch, ci, cl, cm, cn, co, cr, cu, cw, cy, cz, de, dk, dm, do, dz, ec, ee, eg, es, et, fi, fj, fr, gd, ge, gh, gr, gt, hn, hr, ht, hu, id, ie, il, in, iq, ir, is, it, jm, jo, jp, ke, kg, kn, kr, kw, ky, kz, lb, lc, lk, lt, lu, lv, ly, ma, md, me, mk, ml, mm, mn, ms, mt, mx, my, mz, ne, ng, ni, nl, no, nz, om, pa, pe, ph, pk, pl, pt, py, qa, ro, rs, ru, rw, sa, sd, se, sg, si, sk, sn, so, sv, sx, sy, tc, td, th, tn, tr, tt, tz, ua, ug, uk, us, uy, uz, vc, ve, vg, vn, xk, za, zw
- `national-variables/<COUNTRY>.json` - reference values formula-based requirements peg to
- `scripts/validate.py` - CI validator

## Contributing
See CONTRIBUTING.md. Short version: any change to a threshold value needs a real tier-1 source link, or it will not pass CI.
