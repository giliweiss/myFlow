"""Tests for target exercise detection."""

from uuid import uuid4

from app.services.target_exercise_detector import detect_target_exercise, resolve_target_from_clarification
from app.schemas.lesson_generation import ClarificationAnswer


def make_exercise(name_en: str, *, difficulty_level: str = "intermediate") -> dict:
    return {
        "id": str(uuid4()),
        "name_en": name_en,
        "name_he": name_en,
        "canonical_key": name_en.lower().replace(" ", "_"),
        "aliases_en": [],
        "aliases_he": [],
        "difficulty_level": difficulty_level,
    }


def test_detect_target_exercise_finds_named_exercise():
    teaser = make_exercise("Teaser", difficulty_level="advanced")
    catalog = [teaser, make_exercise("Roll Up")]

    result = detect_target_exercise("Prepare the group for Teaser", catalog, "intermediate")

    assert result.target_exercise == teaser
    assert result.target_above_group_level is True


def test_detect_target_exercise_returns_ambiguous_matches():
    first_roll_up = make_exercise("Roll Up")
    second_roll_up = make_exercise("Roll Up")
    catalog = [first_roll_up, second_roll_up]

    result = detect_target_exercise("Work toward Roll Up", catalog, "beginner")

    assert result.target_exercise is None
    assert len(result.ambiguous_matches) == 2


def test_resolve_target_from_clarification_uses_answer():
    alpha = make_exercise("Alpha Roll")
    beta = make_exercise("Beta Roll")

    resolved = resolve_target_from_clarification(
        "Work toward roll",
        [ClarificationAnswer(question_id="ambiguous_target", answer="Alpha Roll")],
        [alpha, beta],
    )

    assert resolved == alpha
