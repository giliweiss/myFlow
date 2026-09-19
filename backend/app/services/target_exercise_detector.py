from dataclasses import dataclass, field

from app.services.exercise_filter import LEVEL_RANK


@dataclass
class TargetDetectionResult:
    target_exercise: dict | None = None
    ambiguous_matches: list[dict] = field(default_factory=list)
    target_above_group_level: bool = False


def _exercise_search_terms(exercise: dict) -> list[str]:
    terms = [
        exercise.get("name_en") or "",
        exercise.get("name_he") or "",
        exercise.get("canonical_key") or "",
    ]
    terms.extend(exercise.get("aliases_en") or [])
    terms.extend(exercise.get("aliases_he") or [])
    return [term.casefold().strip() for term in terms if term and term.strip()]


def detect_target_exercise(
    intention: str,
    full_catalog: list[dict],
    group_level: str,
) -> TargetDetectionResult:
    normalized_intention = intention.casefold()
    if not normalized_intention.strip():
        return TargetDetectionResult()

    matched_exercises: list[dict] = []
    for exercise in full_catalog:
        for term in _exercise_search_terms(exercise):
            if len(term) >= 3 and term in normalized_intention:
                matched_exercises.append(exercise)
                break

    if not matched_exercises:
        return TargetDetectionResult()

    unique_matches = {exercise["id"]: exercise for exercise in matched_exercises}
    matches = list(unique_matches.values())

    if len(matches) > 1:
        return TargetDetectionResult(ambiguous_matches=matches)

    target_exercise = matches[0]
    return TargetDetectionResult(
        target_exercise=target_exercise,
        target_above_group_level=_is_above_group_level(target_exercise, group_level),
    )


def resolve_target_from_clarification(
    intention: str,
    clarification_answers: list,
    ambiguous_matches: list[dict],
) -> dict | None:
    combined_text = intention.casefold()
    for answer in clarification_answers:
        if answer.answer.strip():
            combined_text = f"{combined_text} {answer.answer.casefold()}"

    for exercise in ambiguous_matches:
        for term in _exercise_search_terms(exercise):
            if len(term) >= 3 and term in combined_text:
                return exercise

    return None


def _is_above_group_level(target_exercise: dict, group_level: str) -> bool:
    exercise_level = target_exercise.get("difficulty_level")
    if exercise_level not in LEVEL_RANK or group_level not in LEVEL_RANK:
        return False
    return LEVEL_RANK[exercise_level] > LEVEL_RANK[group_level]
