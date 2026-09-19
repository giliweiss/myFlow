from uuid import UUID

from fastapi import HTTPException, status

from app.schemas.lesson_generation import (
    ClarificationQuestion,
    GeneratedExerciseAlternative,
    GeneratedExerciseGuidance,
    GeneratedLessonExercise,
    GeneratedLessonGuidance,
    GenerateLessonClarificationResponse,
    GenerateLessonReadyResponse,
)
from app.schemas.llm_lesson_plan import (
    LLMClarificationOutput,
    LLMPlanningOutput,
    LLMReadyLessonPlan,
)
from app.services.lesson_validator import VALID_SECTIONS


def validate_llm_lesson_plan(
    plan: LLMReadyLessonPlan,
    allowed_exercise_ids: set[str],
) -> None:
    issues: list[str] = []

    if not plan.title.strip():
        issues.append("title is required")

    if not plan.primary_goal.strip():
        issues.append("primary_goal is required")

    if not plan.lesson_exercises:
        issues.append("at least one exercise is required")

    order_indexes = [exercise.order_index for exercise in plan.lesson_exercises]
    if len(order_indexes) != len(set(order_indexes)):
        issues.append("order_index values must be unique within the lesson")

    expected_order = list(range(len(plan.lesson_exercises)))
    if sorted(order_indexes) != expected_order:
        issues.append("order_index values must be sequential starting at 0")

    for exercise in plan.lesson_exercises:
        if exercise.section not in VALID_SECTIONS:
            issues.append(f"Invalid section: {exercise.section}")
        if exercise.exercise_id not in allowed_exercise_ids:
            issues.append(f"Unknown exercise_id: {exercise.exercise_id}")
        for alternative in exercise.alternatives:
            if alternative.exercise_id not in allowed_exercise_ids:
                issues.append(f"Unknown alternative exercise_id: {alternative.exercise_id}")

    for guidance in plan.guidance.exercise_guidance:
        if guidance.exercise_id not in allowed_exercise_ids:
            issues.append(f"Unknown guidance exercise_id: {guidance.exercise_id}")

    if issues:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"message": "Generated lesson plan failed validation", "issues": issues},
        )


def build_clarification_response(
    group_id: str,
    clarification_output: LLMClarificationOutput | LLMPlanningOutput,
) -> GenerateLessonClarificationResponse:
    if isinstance(clarification_output, LLMPlanningOutput):
        questions_source = clarification_output.clarification_questions
    else:
        questions_source = clarification_output.clarification_questions

    questions = [
        ClarificationQuestion(
            question_id=question.question_id,
            prompt=question.prompt,
            why_needed=question.why_needed,
        )
        for question in questions_source
    ]

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Clarification response is missing questions",
        )

    return GenerateLessonClarificationResponse(
        group_id=UUID(group_id),
        clarification_questions=questions,
    )


def build_ready_lesson_response(
    group_id: str,
    request_notes: str | None,
    planned_duration_minutes: int,
    plan: LLMReadyLessonPlan,
) -> GenerateLessonReadyResponse:
    lesson_exercises = [
        GeneratedLessonExercise(
            exercise_id=UUID(exercise.exercise_id),
            order_index=exercise.order_index,
            section=exercise.section,
            planned_duration_seconds=exercise.planned_duration_seconds,
            sets=exercise.sets,
            reps=exercise.reps,
            selected_modification=exercise.selected_modification,
            instructor_notes=exercise.instructor_notes,
            alternatives=[
                GeneratedExerciseAlternative(
                    exercise_id=UUID(alternative.exercise_id),
                    relation_type=alternative.relation_type,
                    reason=alternative.reason,
                )
                for alternative in exercise.alternatives
            ],
        )
        for exercise in plan.lesson_exercises
    ]

    guidance = GeneratedLessonGuidance(
        lesson_strategy=plan.guidance.lesson_strategy,
        structure_rationale=plan.guidance.structure_rationale,
        progression_logic=plan.guidance.progression_logic,
        section_notes={
            section_note.section: section_note.note for section_note in plan.guidance.section_notes
        },
        exercise_guidance=[
            GeneratedExerciseGuidance(
                exercise_id=UUID(item.exercise_id),
                why_chosen=item.why_chosen,
                progression_role=item.progression_role,
                teaching_cues=item.teaching_cues,
                creative_variations=item.creative_variations,
            )
            for item in plan.guidance.exercise_guidance
        ],
    )

    return GenerateLessonReadyResponse(
        group_id=UUID(group_id),
        title=plan.title.strip(),
        primary_goal=plan.primary_goal.strip(),
        secondary_goals=plan.secondary_goals,
        planned_duration_minutes=planned_duration_minutes,
        instructor_notes=request_notes,
        lesson_exercises=lesson_exercises,
        guidance=guidance,
    )


def planning_output_to_ready_plan(planning_output: LLMPlanningOutput) -> LLMReadyLessonPlan:
    if planning_output.status != "ready":
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Planning output is not ready",
        )

    if not planning_output.title or not planning_output.primary_goal or planning_output.guidance is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ready planning output is missing required fields",
        )

    return LLMReadyLessonPlan(
        title=planning_output.title,
        primary_goal=planning_output.primary_goal,
        secondary_goals=planning_output.secondary_goals,
        lesson_exercises=planning_output.lesson_exercises,
        guidance=planning_output.guidance,
    )
