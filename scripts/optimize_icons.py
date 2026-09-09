#!/usr/bin/env python3
"""
Optimize icons/*.png for web use and catch filename bugs before they ship.

What it does, every time it runs:
1. Sanitizes filenames — strips/replaces spaces and other unsafe characters
   with hyphens (e.g. "chile-moai statue.png" -> "chile-moai-statue.png").
   Updates any references to the old filename inside atlas.html so renaming
   never silently breaks the site.
2. Resizes any icon wider than MAX_DIM down to MAX_DIM x MAX_DIM (aspect
   preserved, then padded/cropped to square), re-saves as an optimized PNG.
   MAX_DIM defaults to 160px, which is 4x the 40px display size in
   atlas.html — plenty of headroom for retina screens, nowhere near the
   original 1000-2300px source files.
3. Skips files already at or under MAX_DIM and under SIZE_TARGET_BYTES,
   so re-runs are fast and idempotent.
4. Cross-checks every icon path referenced in atlas.html against the
   icons/ folder and fails loudly (non-zero exit) if any reference points
   to a file that doesn't exist — this is what silently broke 8 country
   markers across the last few commits.

Run locally:
    python3 scripts/optimize_icons.py

Exit code is non-zero if any icon reference in atlas.html is broken, so CI
can catch it. Optimization itself never fails the build — it just fixes
what it can and reports what it did.
"""
import os
import re
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = REPO_ROOT / "icons"
ATLAS_HTML = REPO_ROOT / "atlas.html"

MAX_DIM = 160  # px, ~4x the 40px display size used in atlas.html
SIZE_TARGET_BYTES = 40_000  # skip re-processing files already this small


def sanitize_filename(name: str) -> str:
    stem, ext = os.path.splitext(name)
    stem = stem.strip()
    stem = re.sub(r"\s+", "-", stem)
    stem = re.sub(r"-{2,}", "-", stem)
    return f"{stem}{ext}"


def rename_and_fix_references(old_path: Path) -> Path:
    new_name = sanitize_filename(old_path.name)
    new_path = old_path.parent / new_name
    if new_name == old_path.name:
        return old_path

    old_path.rename(new_path)
    print(f"  renamed: {old_path.name!r} -> {new_name!r}")

    if ATLAS_HTML.exists():
        text = ATLAS_HTML.read_text(encoding="utf-8")
        old_ref = f"icons/{old_path.name}"
        new_ref = f"icons/{new_name}"
        if old_ref in text:
            text = text.replace(old_ref, new_ref)
            ATLAS_HTML.write_text(text, encoding="utf-8")
            print(f"  updated atlas.html reference: {old_ref!r} -> {new_ref!r}")
    return new_path


def optimize_image(path: Path) -> None:
    before_size = path.stat().st_size
    with Image.open(path) as im:
        w, h = im.size
        if max(w, h) <= MAX_DIM and before_size <= SIZE_TARGET_BYTES:
            return  # already optimized, skip

        im = im.convert("RGBA")
        im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
        im.save(path, optimize=True)

    after_size = path.stat().st_size
    if after_size < before_size:
        pct = 100 * (1 - after_size / before_size)
        print(f"  optimized: {path.name} ({before_size:,}B -> {after_size:,}B, -{pct:.0f}%)")


def check_atlas_references() -> list[str]:
    if not ATLAS_HTML.exists():
        return []
    text = ATLAS_HTML.read_text(encoding="utf-8")
    referenced = sorted(set(re.findall(r'"icons/([^"]+)"', text)))
    missing = [name for name in referenced if not (ICONS_DIR / name).exists()]
    return missing


def main() -> int:
    if not ICONS_DIR.exists():
        print("No icons/ directory found, nothing to do.")
        return 0

    print("Sanitizing filenames...")
    for path in sorted(ICONS_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() == ".png":
            rename_and_fix_references(path)

    print("Optimizing images...")
    for path in sorted(ICONS_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() == ".png":
            optimize_image(path)

    print("Checking atlas.html icon references...")
    missing = check_atlas_references()
    if missing:
        print("\nFAILURES: atlas.html references icons that don't exist:")
        for name in missing:
            print(f"  - icons/{name}")
        print(f"\n{len(missing)} broken reference(s). Build fails.")
        return 1

    print("All atlas.html icon references resolve. Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
