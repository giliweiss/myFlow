"""Tests for deterministic clarification rules."""

from app.schemas.lesson_generation import ClarificationAnswer, GenerateLessonRequest
from app.services.clarification_rules import evaluate_clarification_rules
from app.services.target_exercise_detector import TargetDetectionResult


def make_group(**overrides) -> dict:
    group = {
        "level": "intermediate",
        "group_considerations": [],
    }
    group.update(overrides)
    return group


def test_vague_intention_forces_clarification():
    request = GenerateLessonRequest(intention="good lesson", planned_duration_minutes=60)
    result = evaluate_clarification_rules(request, make_group(), TargetDetectionResult())

    assert result is not None
    assert result.question_id == "vague_intention"


def test_considerations_unaddressed_forces_clarification():
    request = GenerateLessonRequest(intention="Core stability lesson", planned_duration_minutes=60)
    group = make_group(group_considerations=["neck_sensitivity"])
    result = evaluate_clarification_rules(request, group, TargetDetectionResult())

    assert result is not None
    assert result.question_id == "considerations_unaddressed"


def test_answered_clarification_skips_repeat():
    request = GenerateLessonRequest(
        intention="good lesson",
        planned_duration_minutes=60,
        clarification_answers=[
            ClarificationAnswer(question_id="vague_intention", answer="Hip mobility"),
        ],
    )
    result = evaluate_clarification_rules(request, make_group(), TargetDetectionResult())

    assert result is None
