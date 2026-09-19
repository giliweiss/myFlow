from dataclasses import dataclass, field

from app.schemas.lesson_generation import ClarificationAnswer, GenerateLessonRequest, resolve_intention
from app.services.target_exercise_detector import TargetDetectionResult

GENERIC_INTENTION_PHRASES = (
    "good lesson",
    "nice lesson",
    "great lesson",
    "fun class",
    "good class",
    "make it good",
    "plan a lesson",
)


@dataclass
class ForcedClarification:
    question_id: str
    topic: str
    why_needed: str
    candidates: list[str] = field(default_factory=list)


def evaluate_clarification_rules(
    request: GenerateLessonRequest,
    group: dict,
    target_detection: TargetDetectionResult,
) -> ForcedClarification | None:
    intention = resolve_intention(request)
    answered_question_ids = {
        answer.question_id for answer in request.clarification_answers if answer.answer.strip()
    }
    combined_text = _combined_context_text(intention, request.notes, request.clarification_answers)

    if target_detection.ambiguous_matches and "ambiguous_target" not in answered_question_ids:
        candidate_names = [
            exercise.get("name_en") or exercise.get("name_he") or exercise["id"]
            for exercise in target_detection.ambiguous_matches
        ]
        return ForcedClarification(
            question_id="ambiguous_target",
            topic="Which target exercise do you mean?",
            why_needed="Multiple catalog exercises match the intention.",
            candidates=candidate_names,
        )

    group_considerations = group.get("group_considerations") or []
    if group_considerations and "considerations_unaddressed" not in answered_question_ids:
        if not _considerations_addressed(group_considerations, combined_text):
            return ForcedClarification(
                question_id="considerations_unaddressed",
                topic="How should the lesson adapt to this group's limitations?",
                why_needed="The group has active considerations that were not addressed in the intention.",
                candidates=list(group_considerations),
            )

    if (
        not target_detection.target_exercise
        and not target_detection.ambiguous_matches
        and "vague_intention" not in answered_question_ids
        and _is_vague_intention(intention)
    ):
        return ForcedClarification(
            question_id="vague_intention",
            topic="What should be the main focus of this lesson?",
            why_needed="The intention is too general to plan a purposeful lesson.",
        )

    return None


def _combined_context_text(
    intention: str,
    notes: str | None,
    clarification_answers: list[ClarificationAnswer],
) -> str:
    parts = [intention, notes or ""]
    parts.extend(answer.answer for answer in clarification_answers)
    return " ".join(part.casefold() for part in parts if part)


def _considerations_addressed(group_considerations: list[str], combined_text: str) -> bool:
    for consideration in group_considerations:
        normalized = consideration.casefold().replace("_", " ").strip()
        if normalized and normalized not in combined_text:
            return False
    return True


def _is_vague_intention(intention: str) -> bool:
    normalized = intention.casefold().strip()
    if len(normalized) < 10:
        return True
    return any(phrase in normalized for phrase in GENERIC_INTENTION_PHRASES)
