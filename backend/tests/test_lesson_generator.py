"""Tests for lesson generation orchestration."""

from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.dependencies import get_group_repository, get_lesson_generator_service, get_lesson_repository
from app.core.auth import get_current_user
from app.main import app
from app.schemas.lesson_generation import GenerateLessonRequest, GenerateLessonReadyResponse
from app.schemas.llm_lesson_plan import (
    LLMGeneratedLessonExercise,
    LLMExerciseGuidance,
    LLMLessonGuidance,
    LLMPlanningOutput,
    LLMReadyLessonPlan,
    LLMSectionNote,
)
from app.services.lesson_generator import LessonGeneratorService
from app.services.lesson_planning_context import LessonPlanningContext
from app.services.lesson_validator import VALID_SECTIONS

GROUP_ID = "11111111-1111-1111-1111-111111111111"
INSTRUCTOR_ID = "22222222-2222-2222-2222-222222222222"


def make_exercise(
    name_en: str,
    *,
    difficulty_level: str = "beginner",
    possible_equipment: list[str] | None = None,
) -> dict:
    exercise_id = str(uuid4())
    return {
        "id": exercise_id,
        "canonical_key": name_en.lower().replace(" ", "_"),
        "name_en": name_en,
        "name_he": name_en,
        "difficulty_level": difficulty_level,
        "body_focus": ["core"],
        "position": "supine",
        "possible_equipment": possible_equipment or ["mat"],
        "intensity": 2,
        "min_duration_seconds": 60,
        "max_duration_seconds": 180,
        "min_reps": None,
        "max_reps": None,
        "phase_affinities": [],
        "teaching_cues_en": [],
        "teaching_cues_he": [],
        "common_mistakes_en": [],
        "common_mistakes_he": [],
        "aliases_en": [],
        "aliases_he": [],
        "pilates_principles": [],
        "is_active": True,
    }


def make_group(**overrides) -> dict:
    group = {
        "id": GROUP_ID,
        "instructor_id": INSTRUCTOR_ID,
        "name": "Test Group",
        "level": "intermediate",
        "available_equipment": ["mat"],
        "group_considerations": [],
        "typical_duration_minutes": 60,
    }
    group.update(overrides)
    return group


def make_guidance(exercise_id: str) -> LLMLessonGuidance:
    return LLMLessonGuidance(
        lesson_strategy="Build core stability progressively.",
        structure_rationale="Warmup before peak load.",
        progression_logic="Prepare shoulders before advanced work.",
        section_notes=[LLMSectionNote(section="warmup", note="Keep breath steady.")],
        exercise_guidance=[
            LLMExerciseGuidance(
                exercise_id=exercise_id,
                why_chosen="Accessible entry point.",
                progression_role="Preparation",
                teaching_cues=["Keep ribs soft."],
                creative_variations=["Add arm reach."],
            )
        ],
    )


def make_llm_plan_for_exercises(exercises: list[dict]) -> LLMPlanningOutput:
    lesson_exercises = [
        LLMGeneratedLessonExercise(
            exercise_id=exercise["id"],
            order_index=index,
            section="warmup" if index == 0 else "main" if index == 1 else "cooldown",
            planned_duration_seconds=300,
        )
        for index, exercise in enumerate(exercises[:3])
    ]

    return LLMPlanningOutput(
        status="ready",
        title="Generated Lesson",
        primary_goal="Core stability",
        secondary_goals=["Breathing"],
        lesson_exercises=lesson_exercises,
        guidance=make_guidance(exercises[0]["id"]),
    )


def build_service(exercises: list[dict], llm_service: MagicMock | None = None) -> LessonGeneratorService:
    exercise_repository = MagicMock()
    exercise_repository.list_active.return_value = exercises
    exercise_repository.get_restrictions_by_exercise_ids.return_value = {}
    exercise_repository.get_relations_for_exercise_ids.return_value = []

    mock_llm_service = llm_service or MagicMock()
    if llm_service is None:
        mock_llm_service.generate_lesson_plan.return_value = make_llm_plan_for_exercises(exercises)

    return LessonGeneratorService(exercise_repository, mock_llm_service)


def test_generate_returns_catalog_exercise_ids():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Foxtrot"]]
    service = build_service(exercises)
    request = GenerateLessonRequest(
        intention="Core stability with breathing focus",
        planned_duration_minutes=60,
        notes="Keep it gentle",
    )

    response = service.generate(GROUP_ID, make_group(), request)
    catalog_ids = {exercise["id"] for exercise in exercises}

    assert response.status == "ready"
    assert all(str(item.exercise_id) in catalog_ids for item in response.lesson_exercises)
    assert response.instructor_notes == "Keep it gentle"
    assert response.primary_goal == "Core stability"
    assert response.secondary_goals == ["Breathing"]
    assert response.guidance.lesson_strategy is not None


def test_generate_sections_and_order_index_are_valid():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Foxtrot", "Golf", "Hotel"]]
    service = build_service(exercises)
    request = GenerateLessonRequest(intention="hip mobility and breath", planned_duration_minutes=60)

    response = service.generate(GROUP_ID, make_group(), request)
    order_indexes = [item.order_index for item in response.lesson_exercises]

    assert response.status == "ready"
    assert order_indexes == list(range(len(order_indexes)))
    assert len(order_indexes) == len(set(order_indexes))
    assert all(item.section in VALID_SECTIONS for item in response.lesson_exercises)


def test_generate_response_matches_ready_response_schema():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma", "Delta", "Echo"]]
    service = build_service(exercises)
    request = GenerateLessonRequest(intention="shoulder control and stability", planned_duration_minutes=45)

    response = service.generate(GROUP_ID, make_group(), request)
    validated = GenerateLessonReadyResponse.model_validate(response.model_dump(mode="json"))

    assert validated.group_id == UUID(GROUP_ID)
    assert validated.title == "Generated Lesson"
    assert validated.planned_duration_minutes == 45
    assert len(validated.lesson_exercises) > 0


def test_generate_passes_planning_context_to_llm():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma"]]
    llm_service = MagicMock()
    llm_service.generate_lesson_plan.return_value = make_llm_plan_for_exercises(exercises)
    service = build_service(exercises, llm_service=llm_service)
    group = make_group()
    request = GenerateLessonRequest(intention="balance and control", planned_duration_minutes=60)

    service.generate(GROUP_ID, group, request)

    llm_service.generate_lesson_plan.assert_called_once()
    planning_context = llm_service.generate_lesson_plan.call_args.args[2]
    assert isinstance(planning_context, LessonPlanningContext)
    assert len(planning_context.preparation_catalog) == 3
    assert planning_context.intention == "balance and control"


def test_generate_rejects_invalid_llm_output():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma"]]
    llm_service = MagicMock()
    llm_service.generate_lesson_plan.return_value = LLMPlanningOutput(
        status="ready",
        title="Bad Lesson",
        primary_goal="Core",
        lesson_exercises=[
            LLMGeneratedLessonExercise(
                exercise_id=str(uuid4()),
                order_index=0,
                section="warmup",
            )
        ],
        guidance=make_guidance(str(uuid4())),
    )
    service = build_service(exercises, llm_service=llm_service)

    with pytest.raises(HTTPException) as error:
        service.generate(
            GROUP_ID,
            make_group(),
            GenerateLessonRequest(intention="core stability work", planned_duration_minutes=60),
        )

    assert error.value.status_code == 502


def test_generate_returns_forced_clarification_for_vague_intention():
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma"]]
    llm_service = MagicMock()
    from app.schemas.llm_lesson_plan import LLMClarificationOutput, LLMClarificationQuestion

    llm_service.formulate_clarification_questions.return_value = LLMClarificationOutput(
        clarification_questions=[
            LLMClarificationQuestion(
                question_id="vague_intention",
                prompt="What should be the main focus?",
                why_needed="The intention is too general.",
            )
        ]
    )
    service = build_service(exercises, llm_service=llm_service)

    response = service.generate(
        GROUP_ID,
        make_group(),
        GenerateLessonRequest(intention="good lesson", planned_duration_minutes=60),
    )

    assert response.status == "needs_clarification"
    assert response.clarification_questions[0].question_id == "vague_intention"
    llm_service.generate_lesson_plan.assert_not_called()


def test_generate_loads_target_relations_when_target_detected():
    teaser = make_exercise("Teaser", difficulty_level="advanced")
    prep = make_exercise("Roll Up")
    beta = make_exercise("Beta")
    gamma = make_exercise("Gamma")
    exercises = [teaser, prep, beta, gamma]
    llm_service = MagicMock()
    llm_service.generate_lesson_plan.return_value = make_llm_plan_for_exercises([prep, beta, gamma])

    exercise_repository = MagicMock()
    exercise_repository.list_active.return_value = exercises
    exercise_repository.get_restrictions_by_exercise_ids.return_value = {}
    exercise_repository.get_relations_for_exercise_ids.return_value = [
        {
            "exercise_id": teaser["id"],
            "related_exercise_id": prep["id"],
            "relation_type": "regression",
        }
    ]

    service = LessonGeneratorService(exercise_repository, llm_service)
    service.generate(
        GROUP_ID,
        make_group(),
        GenerateLessonRequest(intention="Prepare the group for Teaser", planned_duration_minutes=60),
    )

    exercise_repository.get_relations_for_exercise_ids.assert_called_once_with([teaser["id"]])


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_endpoint_does_not_create_lesson(client: TestClient):
    exercises = [make_exercise(name) for name in ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Foxtrot"]]
    exercise_repository = MagicMock()
    exercise_repository.list_active.return_value = exercises
    exercise_repository.get_restrictions_by_exercise_ids.return_value = {}
    exercise_repository.get_relations_for_exercise_ids.return_value = []

    llm_service = MagicMock()
    llm_service.generate_lesson_plan.return_value = make_llm_plan_for_exercises(exercises)

    group_repository = MagicMock()
    group_repository.get_by_id.return_value = make_group()

    lesson_repository = MagicMock()
    generator_service = LessonGeneratorService(exercise_repository, llm_service)

    app.dependency_overrides[get_current_user] = lambda: {"user_id": INSTRUCTOR_ID, "email": "test@example.com", "token": None}
    app.dependency_overrides[get_group_repository] = lambda: group_repository
    app.dependency_overrides[get_lesson_repository] = lambda: lesson_repository
    app.dependency_overrides[get_lesson_generator_service] = lambda: generator_service

    try:
        response = client.post(
            f"/groups/{GROUP_ID}/lessons/generate",
            json={
                "intention": "Core stability and breathing",
                "planned_duration_minutes": 60,
                "notes": "Test notes",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    GenerateLessonReadyResponse.model_validate(payload)
    lesson_repository.create.assert_not_called()
    assert len(payload["lesson_exercises"]) > 0
