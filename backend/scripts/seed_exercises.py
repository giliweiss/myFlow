"""
Seed the Pilates exercise catalog into Supabase from bilingual JSON files.

Each exercise is stored once with English and Hebrew localized fields merged
from data/exercises.json and data/exercises_he.json.

Usage (from backend/):
  uv run python scripts/seed_exercises.py
  uv run python scripts/seed_exercises.py --clear
  uv run python scripts/validate_exercise_data.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = SCRIPTS_ROOT.parent
DEFAULT_ENGLISH_PATH = BACKEND_ROOT / "data" / "exercises.json"
DEFAULT_HEBREW_PATH = BACKEND_ROOT / "data" / "exercises_he.json"

RELATION_FIELDS = {
    "progressions": "progression",
    "regressions": "regression",
    "alternatives": "alternative",
}

LANGUAGE_INDEPENDENT_FIELDS = (
    "difficulty_level",
    "body_focus",
    "position",
    "intensity",
    "min_duration_seconds",
    "max_duration_seconds",
    "min_reps",
    "max_reps",
    "pilates_principles",
    "phase_affinities",
)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    exercises_matched: int = 0
    restrictions_count: int = 0
    resolvable_relations: int = 0
    skipped_relations: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


@dataclass
class SeedSummary:
    exercises_upserted: int = 0
    restrictions_inserted: int = 0
    relations_inserted: int = 0
    skipped_relations: list[str] = field(default_factory=list)


def load_json_file(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")
    return data


def build_canonical_key(name: str) -> str:
    normalized_name = name.casefold().strip()
    canonical_key = re.sub(r"[^a-z0-9]+", "_", normalized_name)
    return canonical_key.strip("_")


def get_possible_equipment(exercise: dict) -> list[str]:
    equipment = exercise.get("possible_equipment")
    if equipment is None:
        equipment = exercise.get("possiple_equipment")
    return equipment or []


def normalize_string_list(values: list[str] | None) -> list[str]:
    if not values:
        return []

    normalized_values: list[str] = []
    seen: set[str] = set()

    for value in values:
        cleaned_value = value.strip()
        if not cleaned_value:
            continue
        key = cleaned_value.casefold()
        if key in seen:
            continue
        seen.add(key)
        normalized_values.append(cleaned_value)

    return normalized_values


def index_exercises_by_name(exercises: list[dict], source_label: str) -> dict[str, dict]:
    indexed_exercises: dict[str, dict] = {}

    for exercise in exercises:
        exercise_name = exercise.get("name")
        if not exercise_name:
            raise ValueError(f"{source_label} file contains an exercise without a name")

        if exercise_name in indexed_exercises:
            raise ValueError(
                f"{source_label} file contains duplicate exercise name: {exercise_name!r}"
            )

        indexed_exercises[exercise_name] = exercise

    return indexed_exercises


def validate_language_independent_fields(
    canonical_name: str,
    english_exercise: dict,
    hebrew_exercise: dict,
    report: ValidationReport,
) -> None:
    for field_name in LANGUAGE_INDEPENDENT_FIELDS:
        english_value = english_exercise.get(field_name)
        hebrew_value = hebrew_exercise.get(field_name)

        if english_value != hebrew_value:
            report.errors.append(
                f"{canonical_name}: language-independent field {field_name!r} differs "
                f"between English and Hebrew files"
            )

    english_equipment = get_possible_equipment(english_exercise)
    hebrew_equipment = get_possible_equipment(hebrew_exercise)
    if english_equipment != hebrew_equipment:
        report.errors.append(
            f"{canonical_name}: possible_equipment differs between English and Hebrew files"
        )


def validate_restrictions(
    canonical_name: str,
    english_exercise: dict,
    hebrew_exercise: dict,
    report: ValidationReport,
) -> None:
    english_restrictions = english_exercise.get("restrictions") or []
    hebrew_restrictions = hebrew_exercise.get("restrictions") or []

    english_keys = [restriction["key"] for restriction in english_restrictions]
    hebrew_keys = [restriction["key"] for restriction in hebrew_restrictions]

    if english_keys != hebrew_keys:
        report.errors.append(
            f"{canonical_name}: restriction keys differ between English and Hebrew files"
        )
        return

    english_by_key = {restriction["key"]: restriction for restriction in english_restrictions}
    hebrew_by_key = {restriction["key"]: restriction for restriction in hebrew_restrictions}

    for restriction_key in english_keys:
        english_restriction = english_by_key[restriction_key]
        hebrew_restriction = hebrew_by_key[restriction_key]

        if english_restriction.get("compatibility") != hebrew_restriction.get("compatibility"):
            report.errors.append(
                f"{canonical_name}: compatibility for restriction {restriction_key!r} "
                f"differs between English and Hebrew files"
            )


def pair_exercise_files(
    english_path: Path,
    hebrew_path: Path,
) -> tuple[list[tuple[dict, dict]], ValidationReport]:
    english_exercises = load_json_file(english_path)
    hebrew_exercises = load_json_file(hebrew_path)
    report = ValidationReport()

    english_by_name = index_exercises_by_name(english_exercises, "English")
    hebrew_by_name = index_exercises_by_name(hebrew_exercises, "Hebrew")

    english_names = set(english_by_name)
    hebrew_names = set(hebrew_by_name)

    missing_in_hebrew = sorted(english_names - hebrew_names)
    missing_in_english = sorted(hebrew_names - english_names)

    for exercise_name in missing_in_hebrew:
        report.errors.append(
            f"Exercise {exercise_name!r} exists in English file but is missing in Hebrew file"
        )

    for exercise_name in missing_in_english:
        report.errors.append(
            f"Exercise {exercise_name!r} exists in Hebrew file but is missing in English file"
        )

    paired_exercises: list[tuple[dict, dict]] = []

    for exercise_name in sorted(english_names & hebrew_names):
        english_exercise = english_by_name[exercise_name]
        hebrew_exercise = hebrew_by_name[exercise_name]

        validate_language_independent_fields(
            exercise_name,
            english_exercise,
            hebrew_exercise,
            report,
        )
        validate_restrictions(
            exercise_name,
            english_exercise,
            hebrew_exercise,
            report,
        )

        paired_exercises.append((english_exercise, hebrew_exercise))

    report.exercises_matched = len(paired_exercises)
    return paired_exercises, report


def build_name_lookup(paired_exercises: list[tuple[dict, dict]]) -> dict[str, str]:
    lookup: dict[str, str] = {}

    for english_exercise, _ in paired_exercises:
        canonical_name = english_exercise["name"]
        lookup[canonical_name.casefold()] = canonical_name

        for alias in english_exercise.get("aliases", []):
            lookup[alias.casefold()] = canonical_name

    return lookup


def resolve_exercise_name(label: str, lookup: dict[str, str]) -> str | None:
    normalized_label = label.strip().rstrip(".")
    if not normalized_label:
        return None
    return lookup.get(normalized_label.casefold())


def build_exercise_row(english_exercise: dict, hebrew_exercise: dict) -> dict:
    canonical_name = english_exercise["name"]

    return {
        "canonical_key": build_canonical_key(canonical_name),
        "name_en": canonical_name,
        "name_he": hebrew_exercise.get("name_he") or hebrew_exercise["name"],
        "description_en": english_exercise.get("description"),
        "description_he": hebrew_exercise.get("description"),
        "difficulty_level": english_exercise["difficulty_level"],
        "body_focus": english_exercise.get("body_focus") or [],
        "position": english_exercise.get("position"),
        "possible_equipment": get_possible_equipment(english_exercise),
        "intensity": english_exercise.get("intensity"),
        "min_duration_seconds": english_exercise.get("min_duration_seconds"),
        "max_duration_seconds": english_exercise.get("max_duration_seconds"),
        "min_reps": english_exercise.get("min_reps"),
        "max_reps": english_exercise.get("max_reps"),
        "phase_affinities": english_exercise.get("phase_affinities") or [],
        "teaching_cues_en": english_exercise.get("teaching_cues") or [],
        "teaching_cues_he": hebrew_exercise.get("teaching_cues") or [],
        "common_mistakes_en": english_exercise.get("common_mistakes") or [],
        "common_mistakes_he": hebrew_exercise.get("common_mistakes") or [],
        "aliases_en": normalize_string_list(english_exercise.get("aliases")),
        "aliases_he": normalize_string_list(hebrew_exercise.get("aliases")),
        "pilates_principles": english_exercise.get("pilates_principles") or [],
        "is_active": True,
    }


def build_restriction_rows(
    exercise_id: str,
    english_exercise: dict,
    hebrew_exercise: dict,
) -> list[dict]:
    english_restrictions = {
        restriction["key"]: restriction
        for restriction in (english_exercise.get("restrictions") or [])
    }
    hebrew_restrictions = {
        restriction["key"]: restriction
        for restriction in (hebrew_exercise.get("restrictions") or [])
    }

    rows: list[dict] = []

    for restriction_key, english_restriction in english_restrictions.items():
        hebrew_restriction = hebrew_restrictions[restriction_key]
        rows.append(
            {
                "exercise_id": exercise_id,
                "restriction_key": restriction_key,
                "compatibility": english_restriction["compatibility"],
                "modification_notes_en": english_restriction.get("modification"),
                "modification_notes_he": hebrew_restriction.get("modification"),
            }
        )

    return rows


def build_relation_rows(
    exercise_id: str,
    english_exercise: dict,
    lookup: dict[str, str],
    name_to_id: dict[str, str],
    skipped_relations: list[str],
) -> list[dict]:
    rows: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    for source_field, relation_type in RELATION_FIELDS.items():
        for label in english_exercise.get(source_field, []):
            related_name = resolve_exercise_name(label, lookup)
            if related_name is None:
                skipped_relations.append(
                    f"{english_exercise['name']} -> {relation_type}: {label}"
                )
                continue

            related_exercise_id = name_to_id.get(related_name)
            if related_exercise_id is None:
                skipped_relations.append(
                    f"{english_exercise['name']} -> {relation_type}: {label} (missing id)"
                )
                continue

            if related_exercise_id == exercise_id:
                skipped_relations.append(
                    f"{english_exercise['name']} -> {relation_type}: self relation skipped"
                )
                continue

            relation_key = (exercise_id, related_exercise_id, relation_type)
            if relation_key in seen:
                continue

            seen.add(relation_key)
            rows.append(
                {
                    "exercise_id": exercise_id,
                    "related_exercise_id": related_exercise_id,
                    "relation_type": relation_type,
                    "notes": None,
                }
            )

    return rows


def validate_exercise_files(english_path: Path, hebrew_path: Path) -> ValidationReport:
    paired_exercises, report = pair_exercise_files(english_path, hebrew_path)

    if not report.is_valid:
        return report

    lookup = build_name_lookup(paired_exercises)
    name_to_id = {
        english_exercise["name"]: f"placeholder-{index}"
        for index, (english_exercise, _) in enumerate(paired_exercises)
    }

    for english_exercise, hebrew_exercise in paired_exercises:
        build_exercise_row(english_exercise, hebrew_exercise)
        report.restrictions_count += len(english_exercise.get("restrictions") or [])

        relations = build_relation_rows(
            name_to_id[english_exercise["name"]],
            english_exercise,
            lookup,
            name_to_id,
            report.skipped_relations,
        )
        report.resolvable_relations += len(relations)

    return report


def ensure_valid_or_raise(report: ValidationReport) -> None:
    if report.is_valid:
        return

    error_lines = ["Exercise data validation failed:"]
    error_lines.extend(f"  - {error}" for error in report.errors)
    raise ValueError("\n".join(error_lines))


def clear_exercise_catalog(supabase_client) -> None:
    supabase_client.table("exercises").delete().neq(
        "canonical_key",
        "__seed_clear_marker__",
    ).execute()


def seed_exercise_catalog(
    supabase_client,
    english_path: Path,
    hebrew_path: Path,
    clear_existing: bool = False,
) -> SeedSummary:
    paired_exercises, validation_report = pair_exercise_files(english_path, hebrew_path)
    ensure_valid_or_raise(validation_report)

    lookup = build_name_lookup(paired_exercises)
    summary = SeedSummary()

    if clear_existing:
        clear_exercise_catalog(supabase_client)

    name_to_id: dict[str, str] = {}

    for english_exercise, hebrew_exercise in paired_exercises:
        exercise_row = build_exercise_row(english_exercise, hebrew_exercise)
        upsert_result = (
            supabase_client.table("exercises")
            .upsert(exercise_row, on_conflict="canonical_key")
            .execute()
        )

        if not upsert_result.data:
            raise RuntimeError(f"Failed to upsert exercise: {english_exercise['name']}")

        upserted_exercise = upsert_result.data[0]
        exercise_id = upserted_exercise["id"]
        name_to_id[english_exercise["name"]] = exercise_id
        summary.exercises_upserted += 1

        supabase_client.table("exercise_restrictions").delete().eq(
            "exercise_id",
            exercise_id,
        ).execute()

        restrictions = build_restriction_rows(
            exercise_id,
            english_exercise,
            hebrew_exercise,
        )
        if restrictions:
            supabase_client.table("exercise_restrictions").insert(restrictions).execute()
            summary.restrictions_inserted += len(restrictions)

    supabase_client.table("exercise_relations").delete().in_(
        "relation_type",
        ["regression", "progression", "alternative"],
    ).execute()

    for english_exercise, _ in paired_exercises:
        exercise_id = name_to_id[english_exercise["name"]]
        relations = build_relation_rows(
            exercise_id,
            english_exercise,
            lookup,
            name_to_id,
            summary.skipped_relations,
        )
        if relations:
            supabase_client.table("exercise_relations").insert(relations).execute()
            summary.relations_inserted += len(relations)

    return summary


def print_validation_report(report: ValidationReport) -> None:
    if not report.is_valid:
        print("Validation failed.")
        for error in report.errors:
            print(f"  - {error}")
        return

    print("Validation passed.")
    print(f"Matched exercises: {report.exercises_matched}")
    print(f"Restrictions: {report.restrictions_count}")
    print(f"Resolvable relations: {report.resolvable_relations}")
    print(f"Skipped relation labels: {len(report.skipped_relations)}")

    if report.skipped_relations:
        print("\nRelation labels that will not be inserted:")
        for item in report.skipped_relations[:20]:
            print(f"  - {item}")
        if len(report.skipped_relations) > 20:
            print(f"  ... and {len(report.skipped_relations) - 20} more")


def print_seed_summary(summary: SeedSummary) -> None:
    print(f"Exercises upserted: {summary.exercises_upserted}")
    print(f"Restrictions inserted: {summary.restrictions_inserted}")
    print(f"Relations inserted: {summary.relations_inserted}")

    if summary.skipped_relations:
        print(f"\nSkipped relation labels ({len(summary.skipped_relations)}):")
        for item in summary.skipped_relations[:20]:
            print(f"  - {item}")
        if len(summary.skipped_relations) > 20:
            print(f"  ... and {len(summary.skipped_relations) - 20} more")


def main() -> None:
    sys.path.insert(0, str(BACKEND_ROOT))

    parser = argparse.ArgumentParser(description="Seed exercises into Supabase")
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
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete existing exercise catalog rows before seeding",
    )
    args = parser.parse_args()

    if not args.english.exists():
        print(f"English file not found: {args.english}")
        sys.exit(1)

    if not args.hebrew.exists():
        print(f"Hebrew file not found: {args.hebrew}")
        sys.exit(1)

    validation_report = validate_exercise_files(args.english, args.hebrew)
    print_validation_report(validation_report)

    if not validation_report.is_valid:
        sys.exit(1)

    from app.core.config import settings
    from supabase import create_client

    supabase_client = create_client(
        settings.supabase_url,
        settings.supabase_service_key,
    )

    print("\nSeeding exercise catalog...")
    if args.clear:
        print("Clearing existing exercise catalog first...")

    summary = seed_exercise_catalog(
        supabase_client,
        args.english,
        args.hebrew,
        clear_existing=args.clear,
    )

    print_seed_summary(summary)
    print("\nDone.")


if __name__ == "__main__":
    main()
