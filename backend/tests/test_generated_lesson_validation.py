"""Tests for generated lesson validation and orchestration."""

from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.schemas.llm_lesson_plan import LLMGeneratedLessonExercise, LLMGeneratedLessonPlan, LLMLessonGuidance
from app.services.generated_lesson_validation import validate_llm_lesson_plan


def test_validate_llm_lesson_plan_rejects_unknown_exercise_id():
    allowed_id = str(uuid4())
    unknown_id = str(uuid4())
    plan = LLMGeneratedLessonPlan(
        title="Test Lesson",
        primary_goal="Core",
        lesson_exercises=[
            LLMGeneratedLessonExercise(
                exercise_id=unknown_id,
                order_index=0,
                section="warmup",
            )
        ],
        guidance=LLMLessonGuidance(),
    )

    with pytest.raises(HTTPException) as error:
        validate_llm_lesson_plan(plan, {allowed_id})

    assert error.value.status_code == 502
    assert "Unknown exercise_id" in str(error.value.detail)


def test_validate_llm_lesson_plan_rejects_invalid_order_index():
    exercise_id = str(uuid4())
    plan = LLMGeneratedLessonPlan(
        title="Test Lesson",
        primary_goal="Core",
        lesson_exercises=[
            LLMGeneratedLessonExercise(
                exercise_id=exercise_id,
                order_index=1,
                section="warmup",
            )
        ],
        guidance=LLMLessonGuidance(),
    )

    with pytest.raises(HTTPException) as error:
        validate_llm_lesson_plan(plan, {exercise_id})

    assert error.value.status_code == 502
    assert "sequential" in str(error.value.detail)
