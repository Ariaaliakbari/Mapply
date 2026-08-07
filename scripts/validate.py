#!/usr/bin/env python3
"""
Mapply route validator.

Checks every file in routes/**/*.json against schema/route.schema.json, plus
rules that plain JSON Schema can't express:

  1. Every 'hard' requirement must cite a source with tier == 1 (government).
  2. verified_at must not be more than 180 days old (fail) or 90 days (warn).
  3. Every source_id referenced by a requirement must exist in that route's
     own sources list.
  4. Every route id referenced in prerequisites / switchable_to must exist
     somewhere in the routes/ directory (cross-reference check).

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

FAIL_AFTER_DAYS = 180
WARN_AFTER_DAYS = 90


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def find_route_files():
    return sorted(ROUTES_DIR.rglob("*.json"))


def check_schema(route, filepath, schema, errors):
    validator = jsonschema.Draft7Validator(schema)
    for err in validator.iter_errors(route):
        loc = " -> ".join(str(p) for p in err.path) or "(root)"
        errors.append(f"[{filepath.name}] SCHEMA: {loc}: {err.message}")


def check_hard_requirements_tier1(route, filepath, errors):
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
        check_hard_requirements_tier1(route, filepath, errors)
        check_source_ids_exist(route, filepath, errors)
        check_freshness(route, filepath, errors, warnings)

        rid = route.get("id")
        if rid:
            if rid in all_routes_by_id:
                errors.append(f"[{filepath.name}] DUPLICATE id '{rid}'")
            all_routes_by_id[rid] = (filepath, route)

    check_cross_references(all_routes_by_id, errors)

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
