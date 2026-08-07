# Contributing to Mapply

## The one rule that matters

Any **hard requirement** (anything that can disqualify someone) must cite a **tier-1 source** — an official government publication. Not a law firm, not a relocation blog, not a forum. The validator will reject the pull request otherwise.

Source tiers:
- **1** — government (e.g. gov.uk, canada.ca, official ministry sites)
- **2** — intergovernmental (e.g. EU, UN bodies)
- **3** — law firm / relocation consultancy
- **4** — other (news, forums, blogs)

Tiers 2–4 are fine for context, background, or `notes` fields. Never for a hard requirement's `source_id`.

## Adding or editing a route

1. Copy the structure of an existing route file (e.g. `routes/uk/skilled_worker.json`) as your starting point
2. Follow `schema/route.schema.json` exactly — every required field, no exceptions
3. Set `verified_at` to the date you actually checked the source, in `YYYY-MM-DD` format
4. Every requirement needs a plain-language `blocker_text` — written for someone who doesn't know immigration jargon
5. If a requirement is fixable, fill in `fix_path` and a realistic `fix_time_months`. If it isn't (e.g. age, nationality), set both to `null`
6. Run `python3 scripts/validate.py` locally before opening a pull request — it's the same check CI runs

## Adding a new country from scratch

Draft status exists for exactly this. If you can't yet find tier-1 sources for every hard requirement, set `"status": "draft"`. Draft routes validate structurally and live in the repo, but won't be shown publicly until real government sources are attached. Swapping a placeholder for a real citation and flipping status to `"published"` is one of the most useful single contributions possible.

## What we're not accepting

- Personal opinions on chances of success
- Anything without a source
- New applicant attributes without discussion first (the closed list of attributes is a schema-level decision, not a casual addition — open an issue)
