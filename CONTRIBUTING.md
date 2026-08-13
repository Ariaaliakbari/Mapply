# Contributing to Mapply

## The one rule that matters

Any **hard requirement** (anything that can disqualify someone) must cite a **tier-1 source** — an official government publication. Not a law firm, not a relocation blog, not a forum. The validator will reject the pull request otherwise.

Source tiers:
- **1** — government (e.g. gov.uk, canada.ca, gesetze-im-internet.de, bamf.de, official ministry sites)
- **2** — intergovernmental (e.g. EU, UN bodies)
- **3** — law firm / relocation consultancy
- **4** — other (news, forums, blogs)

Tiers 2–4 are fine for context, background, or `notes` fields. Never for a hard requirement's `source_id`.

## Adding or editing a route

1. Copy the structure of an existing route file in the same country as your starting point (`routes/uk/skilled_worker.json` or `routes/de/eu_blue_card.json` are good full examples)
2. Follow `schema/route.schema.json` exactly — every required field, no exceptions
3. Set `verified_at` to the date you actually checked the source, in `YYYY-MM-DD` format
4. Every requirement needs a plain-language `blocker_text` — written for someone who doesn't know immigration jargon
5. If a requirement is fixable, fill in `fix_path` and a realistic `fix_time_months`. If it isn't (e.g. age, nationality), set both to `null`
6. Run `python3 scripts/validate.py` locally before opening a pull request — it's the same check CI runs

## Schema features you might need

**A threshold that's a percentage of a periodically-updated government figure** (e.g. a salary pegged to a minimum wage or pension ceiling): don't hardcode the number. Add or update the relevant entry in `national-variables/<country>.json`, then reference it from the requirement:
```json
"value": { "value_type": "formula", "formula_ref": "<variable_id>", "ratio": 0.5, "resolved_amount": <current computed number>, "currency": "EUR" }
```
CI checks `resolved_amount` actually matches `ratio * variable value` and fails the build if they've drifted apart.

**A route with real internal tiers that lead to different outcomes** (e.g. two ways to qualify with different settlement timelines): use `outcome_override` or `prerequisites_override` on the specific `RequirementGroup`, not a route-level guess. Only include the fields that actually differ — everything else inherits the route-level value.

**A route that's closed to new applicants**: set `"status": "closed"`, `"closed_date"` (required, not null), and `"superseded_by"` (the successor route's id, or explicitly `null` if there isn't one). Don't delete the file — someone may search for a route that no longer exists, and a clear closure notice pointing to the replacement is more useful than nothing.

**A mandatory fee paid to someone other than the government** (an endorsing body, a degree-verification service, a chamber of commerce): add it to the route-level `third_party_fees[]` array. Government application fees don't have a formal field yet — they currently live in `notes`.

## Adding a new country from scratch

Draft status exists for exactly this. If you can't yet find tier-1 sources for every hard requirement, set `"status": "draft"`. Draft routes validate structurally and live in the repo, but won't be shown publicly until real government sources are attached. Swapping a placeholder for a real citation and flipping status to `"published"` is one of the most useful single contributions possible.

If any requirement in the new country needs a formula-valued threshold, add a `national-variables/<COUNTRY>.json` file following `schema/national_variable.schema.json`.

## What we're not accepting

- Personal opinions on chances of success
- Anything without a source
- New applicant attributes without discussion first (the closed list of attributes is a schema-level decision, not a casual addition — open an issue)
