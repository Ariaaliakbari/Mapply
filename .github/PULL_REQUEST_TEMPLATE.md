## What changed

<!-- One or two sentences: which route(s), what field(s), why. -->

## Source

<!-- Required for ANY change to a threshold, fee, duration, or eligibility rule.
     Link the specific government page, not just the domain. -->

- Tier-1 source URL:
- Date accessed:

## Checklist

- [ ] `python3 scripts/validate.py` passes locally
- [ ] Every changed/added hard requirement cites a tier-1 `source_id`
- [ ] `verified_at` is set to the date I actually checked the source
- [ ] If this route is closing, `status`/`closed_date`/`superseded_by` are all set
- [ ] If this is a formula-valued threshold, `national-variables/<country>.json` is updated and `resolved_amount` matches
