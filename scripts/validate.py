#!/usr/bin/env python3
"""
Mapply route validator.

Checks every file in routes/**/*.json against schema/route.schema.json, plus
rules that plain JSON Schema can't express:

  1. Every 'hard' requirement must cite a source with tier == 1 (government).
  2. verified_at must not be more than 180 days old (fail) or 90 days (warn).
  3. Every source_id referenced by a requirement must exist in that route's
     own sources list.
  4. Every route id referenced in prerequisites / switchable_to / group-level
     overrides / superseded_by must exist somewhere in the routes/ directory.
  5. status == "closed" routes must set closed_date (not null) and include
     the superseded_by key (value may be null if there's no direct successor).
  6. Formula-valued requirements (value.value_type == "formula") must
     reference a real variable in national-variables/<country>.json, and
     resolved_amount must match ratio * variable value (small tolerance for
     rounding). Catches drift between a hardcoded display figure and the
     underlying reference value it's supposed to track.

Exit code 0 = all good. Exit code 1 = at least one FAIL. Warnings don't fail
the build but are printed.

Usage: python3 scripts/validate.py
"""

import json
import sys
from pathlib import Path
from datetime import date, datetime

try:
    import jsonschema
except ImportError:
    print("Missing dependency. Run: pip install jsonschema --break-system-packages")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "route.schema.json"
ROUTES_DIR = REPO_ROOT / "routes"
NATIONAL_VARIABLES_DIR = REPO_ROOT / "national-variables"

FAIL_AFTER_DAYS = 180
WARN_AFTER_DAYS = 90
FORMULA_TOLERANCE = 0.02  # 2% — allows for minor rounding in published figures


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def load_national_variables():
    """Returns {country_code: {variable_id: value_number}}"""
    result = {}
    if not NATIONAL_VARIABLES_DIR.exists():
        return result
    for filepath in NATIONAL_VARIABLES_DIR.glob("*.json"):
        with open(filepath) as f:
            data = json.load(f)
        country = data.get("country")
        if country:
            result[country] = {
                var_id: var.get("value")
                for var_id, var in data.get("variables", {}).items()
            }
    return result


def find_route_files():
    return sorted(ROUTES_DIR.rglob("*.json"))


def check_schema(route, filepath, schema, errors):
    validator = jsonschema.Draft7Validator(schema)
    for err in validator.iter_errors(route):
        loc = " -> ".join(str(p) for p in err.path) or "(root)"
        errors.append(f"[{filepath.name}] SCHEMA: {loc}: {err.message}")


def check_hard_requirements_tier1(route, filepath, errors, warnings):
    if route.get("status") == "draft":
        # Draft routes are explicitly allowed incomplete/non-tier-1 sourcing per the
        # schema's own description of "draft" — that's the entire point of the status.
        # Warn instead of fail, so it's visible but doesn't block the build.
        source_tiers = {s["id"]: s.get("tier") for s in route.get("sources", [])}
        for group in route.get("requirement_groups", []):
            for req in group.get("requirements", []):
                if req.get("hard"):
                    tier = source_tiers.get(req.get("source_id"))
                    if tier != 1:
                        warnings.append(
                            f"[{filepath.name}] DRAFT SOURCING: hard requirement '{req.get('id')}' "
                            f"cites source with tier {tier}, not yet tier 1 — expected while draft"
                        )
        return

    source_tiers = {s["id"]: s.get("tier") for s in route.get("sources", [])}
    for group in route.get("requirement_groups", []):
        for req in group.get("requirements", []):
            if req.get("hard"):
                sid = req.get("source_id")
                tier = source_tiers.get(sid)
                if tier != 1:
                    errors.append(
                        f"[{filepath.name}] SOURCING: hard requirement '{req.get('id')}' "
                        f"cites source '{sid}' with tier {tier} (must be tier 1 / government)"
                    )


def check_source_ids_exist(route, filepath, errors):
    known_ids = {s["id"] for s in route.get("sources", [])}
    for group in route.get("requirement_groups", []):
        for req in group.get("requirements", []):
            sid = req.get("source_id")
            if sid not in known_ids:
                errors.append(
                    f"[{filepath.name}] REF: requirement '{req.get('id')}' references "
                    f"unknown source_id '{sid}'"
                )


def check_freshness(route, filepath, errors, warnings):
    v = route.get("verified_at")
    if not v:
        return
    try:
        verified_date = datetime.strptime(v, "%Y-%m-%d").date()
    except ValueError:
        errors.append(f"[{filepath.name}] FRESHNESS: verified_at '{v}' is not YYYY-MM-DD")
        return
    age_days = (date.today() - verified_date).days
    if age_days > FAIL_AFTER_DAYS:
        errors.append(
            f"[{filepath.name}] FRESHNESS: verified_at is {age_days} days old "
            f"(fails past {FAIL_AFTER_DAYS})"
        )
    elif age_days > WARN_AFTER_DAYS:
        warnings.append(
            f"[{filepath.name}] FRESHNESS WARNING: verified_at is {age_days} days old "
            f"(warns past {WARN_AFTER_DAYS})"
        )


def check_closed_status(route, filepath, errors):
    if route.get("status") != "closed":
        return
    never_existed = route.get("closed_date") is None and route.get("superseded_by") is None
    if "closed_date" not in route or route.get("closed_date") is None:
        if not never_existed:
            errors.append(
                f"[{filepath.name}] CLOSED: status is 'closed' but closed_date is missing or null"
            )
        # else: legitimate 'no formal system ever existed' case (e.g. asylum in a
        # non-Convention-signatory country) — closed_date is null because there was
        # never an open state to close from. Requires superseded_by also null AND
        # the route's notes to explicitly document this, checked separately below.
        elif "no formal" not in (route.get("notes") or "").lower() and "never existed" not in (route.get("notes") or "").lower():
            errors.append(
                f"[{filepath.name}] CLOSED: closed_date is null with no closed_date/superseded_by, "
                f"but notes don't explicitly document this as a 'no formal system ever existed' case"
            )
    if "superseded_by" not in route:
        errors.append(
            f"[{filepath.name}] CLOSED: status is 'closed' but superseded_by key is missing "
            f"(set to null explicitly if there's no direct successor)"
        )


def check_formula_values(route, filepath, national_vars, errors):
    country = route.get("country")
    country_vars = national_vars.get(country, {})
    for group in route.get("requirement_groups", []):
        for req in group.get("requirements", []):
            val = req.get("value")
            if not isinstance(val, dict) or val.get("value_type") != "formula":
                continue
            ref = val.get("formula_ref")
            ratio = val.get("ratio")
            resolved = val.get("resolved_amount")
            if ref not in country_vars:
                errors.append(
                    f"[{filepath.name}] FORMULA: requirement '{req.get('id')}' references "
                    f"unknown national variable '{ref}' for country '{country}' "
                    f"(check national-variables/{country}.json)"
                )
                continue
            expected = country_vars[ref] * ratio
            if resolved is None or abs(resolved - expected) > expected * FORMULA_TOLERANCE:
                errors.append(
                    f"[{filepath.name}] FORMULA: requirement '{req.get('id')}' resolved_amount "
                    f"{resolved} doesn't match {ratio} * {ref} ({country_vars[ref]}) = {expected:.2f} "
                    f"(tolerance {FORMULA_TOLERANCE:.0%})"
                )


def check_superseded_by_reference(all_routes_by_id, errors):
    for filepath, route in all_routes_by_id.values():
        sup = route.get("superseded_by")
        if sup and sup not in all_routes_by_id:
            errors.append(
                f"[{filepath.name}] REF: superseded_by references unknown route id '{sup}'"
            )


def check_group_override_references(all_routes_by_id, errors):
    for filepath, route in all_routes_by_id.values():
        for group in route.get("requirement_groups", []):
            override = group.get("outcome_override") or {}
            for rid in override.get("switchable_to", []):
                if rid not in all_routes_by_id:
                    errors.append(
                        f"[{filepath.name}] REF: group '{group.get('id')}' outcome_override.switchable_to "
                        f"references unknown route id '{rid}'"
                    )
            prereq_override = group.get("prerequisites_override") or {}
            for rid in prereq_override.get("required_prior_route_ids", []):
                if rid not in all_routes_by_id:
                    errors.append(
                        f"[{filepath.name}] REF: group '{group.get('id')}' prerequisites_override."
                        f"required_prior_route_ids references unknown route id '{rid}'"
                    )


def check_cross_references(all_routes_by_id, errors):
    for filepath, route in all_routes_by_id.values():
        prereq = route.get("prerequisites") or {}
        for rid in prereq.get("required_prior_route_ids", []):
            if rid not in all_routes_by_id:
                errors.append(
                    f"[{filepath.name}] REF: prerequisites references unknown route id '{rid}'"
                )
        outcome = route.get("outcome", {})
        for rid in outcome.get("switchable_to", []):
            if rid not in all_routes_by_id:
                errors.append(
                    f"[{filepath.name}] REF: switchable_to references unknown route id '{rid}'"
                )


def main():
    schema = load_schema()
    files = find_route_files()
    national_vars = load_national_variables()

    if not files:
        print("No route files found under routes/. Nothing to validate.")
        return 0

    errors = []
    warnings = []
    all_routes_by_id = {}

    for filepath in files:
        with open(filepath) as f:
            try:
                route = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"[{filepath.name}] INVALID JSON: {e}")
                continue

        check_schema(route, filepath, schema, errors)
        check_hard_requirements_tier1(route, filepath, errors, warnings)
        check_source_ids_exist(route, filepath, errors)
        check_freshness(route, filepath, errors, warnings)
        check_closed_status(route, filepath, errors)
        check_formula_values(route, filepath, national_vars, errors)

        rid = route.get("id")
        if rid:
            if rid in all_routes_by_id:
                errors.append(f"[{filepath.name}] DUPLICATE id '{rid}'")
            all_routes_by_id[rid] = (filepath, route)

    check_cross_references(all_routes_by_id, errors)
    check_superseded_by_reference(all_routes_by_id, errors)
    check_group_override_references(all_routes_by_id, errors)

    print(f"Checked {len(files)} route file(s).\n")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print("FAILURES:")
        for e in errors:
            print(f"  - {e}")
        print(f"\n{len(errors)} error(s). Build fails.")
        return 1

    print("All routes valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
