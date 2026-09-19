"""Tests for OpenAIService."""

import json
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.schemas.lesson_generation import GenerateLessonRequest
from app.schemas.llm_lesson_plan import (
    LLMGeneratedLessonExercise,
    LLMExerciseGuidance,
    LLMLessonGuidance,
    LLMPlanningOutput,
)
from app.services.clarification_rules import ForcedClarification
from app.services.lesson_planning_context import LessonPlanningContext
from app.services.openai_service import OpenAIService


def make_exercise(name_en: str) -> dict:
    return {
        "id": str(uuid4()),
        "name_en": name_en,
        "name_he": name_en,
        "difficulty_level": "beginner",
        "body_focus": ["core"],
        "position": "supine",
        "possible_equipment": ["mat"],
        "intensity": 2,
        "min_duration_seconds": 60,
        "max_duration_seconds": 180,
        "min_reps": None,
        "max_reps": None,
    }


def make_group() -> dict:
    return {
        "name": "Test Group",
        "level": "intermediate",
        "available_equipment": ["mat"],
        "group_considerations": [],
        "typical_duration_minutes": 60,
    }


def make_request() -> GenerateLessonRequest:
    return GenerateLessonRequest(
        intention="Core stability and breathing",
        planned_duration_minutes=60,
        notes="Keep it gentle",
    )


def make_plan(exercise_id: str) -> LLMPlanningOutput:
    return LLMPlanningOutput(
        status="ready",
        title="Core Stability Flow",
        primary_goal="Core stability",
        secondary_goals=["Breathing"],
        lesson_exercises=[
            LLMGeneratedLessonExercise(
                exercise_id=exercise_id,
                order_index=0,
                section="warmup",
                planned_duration_seconds=300,
            )
        ],
        guidance=LLMLessonGuidance(
            lesson_strategy="Build from breath.",
            exercise_guidance=[
                LLMExerciseGuidance(
                    exercise_id=exercise_id,
                    why_chosen="Accessible warmup.",
                )
            ],
        ),
    )


def make_planning_context(exercise: dict) -> LessonPlanningContext:
    return LessonPlanningContext(
        intention="Core stability and breathing",
        preparation_catalog=[exercise],
    )


def test_openai_service_raises_when_api_key_missing():
    service = OpenAIService(api_key="", model="gpt-5.6-luna")

    with pytest.raises(HTTPException) as error:
        service.generate_lesson_plan(
            make_group(),
            make_request(),
            make_planning_context(make_exercise("Alpha")),
        )

    assert error.value.status_code == 503


def test_openai_service_calls_responses_parse_with_planning_context():
    exercise = make_exercise("Alpha")
    parsed_response = MagicMock()
    parsed_response.output_parsed = make_plan(exercise["id"])

    mock_client = MagicMock()
    mock_client.responses.parse.return_value = parsed_response

    service = OpenAIService(api_key="test-key", model="gpt-5.6-luna", client=mock_client)
    request = make_request()
    planning_context = make_planning_context(exercise)

    plan = service.generate_lesson_plan(make_group(), request, planning_context)

    mock_client.responses.parse.assert_called_once()
    call_kwargs = mock_client.responses.parse.call_args.kwargs
    assert call_kwargs["model"] == "gpt-5.6-luna"
    assert call_kwargs["text_format"] is LLMPlanningOutput

    user_input = json.loads(call_kwargs["input"])
    assert user_input["lesson_request"]["intention"] == "Core stability and breathing"
    assert len(user_input["preparation_catalog"]) == 1
    assert user_input["preparation_catalog"][0]["id"] == exercise["id"]
    assert plan.title == "Core Stability Flow"


def test_openai_service_raises_when_output_parsed_is_none():
    parsed_response = MagicMock()
    parsed_response.output_parsed = None

    mock_client = MagicMock()
    mock_client.responses.parse.return_value = parsed_response

    service = OpenAIService(api_key="test-key", model="gpt-5.6-luna", client=mock_client)

    with pytest.raises(HTTPException) as error:
        service.generate_lesson_plan(
            make_group(),
            make_request(),
            make_planning_context(make_exercise("Alpha")),
        )

    assert error.value.status_code == 502


def test_openai_service_wraps_openai_errors():
    mock_client = MagicMock()
    mock_client.responses.parse.side_effect = RuntimeError("upstream failure")

    service = OpenAIService(api_key="test-key", model="gpt-5.6-luna", client=mock_client)

    with pytest.raises(HTTPException) as error:
        service.generate_lesson_plan(
            make_group(),
            make_request(),
            make_planning_context(make_exercise("Alpha")),
        )

    assert error.value.status_code == 502
    assert "upstream failure" in str(error.value.detail)


def test_openai_service_formulates_forced_clarification_questions():
    parsed_response = MagicMock()
    from app.schemas.llm_lesson_plan import LLMClarificationOutput, LLMClarificationQuestion

    parsed_response.output_parsed = LLMClarificationOutput(
        clarification_questions=[
            LLMClarificationQuestion(
                question_id="vague_intention",
                prompt="What is the main focus?",
                why_needed="Too general.",
            )
        ]
    )

    mock_client = MagicMock()
    mock_client.responses.parse.return_value = parsed_response

    service = OpenAIService(api_key="test-key", model="gpt-5.6-luna", client=mock_client)
    output = service.formulate_clarification_questions(
        make_group(),
        make_request(),
        [
            ForcedClarification(
                question_id="vague_intention",
                topic="What is the main focus?",
                why_needed="Too general.",
            )
        ],
    )

    assert output.clarification_questions[0].question_id == "vague_intention"
    mock_client.responses.parse.assert_called_once()
