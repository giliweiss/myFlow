"""
Validate English and Hebrew exercise JSON files without touching Supabase.

Usage (from backend/):
  uv run python scripts/validate_exercise_data.py
  uv run python scripts/validate_exercise_data.py --english data/exercises.json --hebrew data/exercises_he.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = SCRIPTS_ROOT.parent
DEFAULT_ENGLISH_PATH = BACKEND_ROOT / "data" / "exercises.json"
DEFAULT_HEBREW_PATH = BACKEND_ROOT / "data" / "exercises_he.json"

sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(SCRIPTS_ROOT))

from seed_exercises import print_validation_report, validate_exercise_files  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate exercise JSON data files")
    parser.add_argument(
        "--english",
        type=Path,
        default=DEFAULT_ENGLISH_PATH,
        help="Path to English exercises JSON",
    )
    parser.add_argument(
        "--hebrew",
        type=Path,
        default=DEFAULT_HEBREW_PATH,
        help="Path to Hebrew exercises JSON",
    )
    args = parser.parse_args()

    if not args.english.exists():
        print(f"English file not found: {args.english}")
        sys.exit(1)

    if not args.hebrew.exists():
        print(f"Hebrew file not found: {args.hebrew}")
        sys.exit(1)

    try:
        report = validate_exercise_files(args.english, args.hebrew)
    except ValueError as error:
        print(error)
        sys.exit(1)

    print_validation_report(report)

    if not report.is_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
