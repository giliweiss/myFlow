from fastapi import HTTPException, status

from app.repositories.exercise_repo import ExerciseRepository
from app.schemas.lesson_generation import (
    GenerateLessonRequest,
    GenerateLessonResponse,
    resolve_intention,
)
from app.services.clarification_rules import evaluate_clarification_rules
from app.services.exercise_filter import LEVEL_RANK, filter_exercises
from app.services.generated_lesson_validation import (
    build_clarification_response,
    build_ready_lesson_response,
    planning_output_to_ready_plan,
    validate_llm_lesson_plan,
)
from app.services.lesson_planning_context import LessonPlanningContext
from app.services.llm_service import LessonGenerationLLM
from app.services.target_exercise_detector import (
    TargetDetectionResult,
    detect_target_exercise,
    resolve_target_from_clarification,
)


class LessonGeneratorService:
    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        llm_service: LessonGenerationLLM,
    ):
        self.exercise_repository = exercise_repository
        self.llm_service = llm_service

    def generate(
        self,
        group_id: str,
        group: dict,
        request: GenerateLessonRequest,
    ) -> GenerateLessonResponse:
        intention = resolve_intention(request)
        if not intention:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="intention is required",
            )

        exercises = self.exercise_repository.list_active()
        exercise_ids = [exercise["id"] for exercise in exercises]
        restrictions = self.exercise_repository.get_restrictions_by_exercise_ids(exercise_ids)

        target_detection = self._resolve_target_detection(intention, exercises, group, request)
        forced_clarification = evaluate_clarification_rules(request, group, target_detection)
        if forced_clarification is not None:
            clarification_output = self.llm_service.formulate_clarification_questions(
                group,
                request,
                [forced_clarification],
            )
            return build_clarification_response(group_id, clarification_output)

        preparation_catalog = filter_exercises(exercises, group, restrictions)
        if not preparation_catalog:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No suitable exercises found for this group",
            )

        target_relations: list[dict] = []
        if target_detection.target_exercise is not None:
            target_relations = self.exercise_repository.get_relations_for_exercise_ids(
                [target_detection.target_exercise["id"]]
            )

        planning_context = LessonPlanningContext(
            intention=intention,
            preparation_catalog=preparation_catalog,
            target_exercise=target_detection.target_exercise,
            target_above_group_level=target_detection.target_above_group_level,
            target_relations=target_relations,
        )

        planning_output = self.llm_service.generate_lesson_plan(group, request, planning_context)
        if planning_output.status == "needs_clarification":
            return build_clarification_response(group_id, planning_output)

        ready_plan = planning_output_to_ready_plan(planning_output)
        allowed_exercise_ids = {exercise["id"] for exercise in preparation_catalog}
        validate_llm_lesson_plan(ready_plan, allowed_exercise_ids)

        return build_ready_lesson_response(
            group_id=group_id,
            request_notes=request.notes,
            planned_duration_minutes=request.planned_duration_minutes,
            plan=ready_plan,
        )

    def _resolve_target_detection(
        self,
        intention: str,
        exercises: list[dict],
        group: dict,
        request: GenerateLessonRequest,
    ) -> TargetDetectionResult:
        group_level = group.get("level") or "beginner"
        target_detection = detect_target_exercise(intention, exercises, group_level)

        if target_detection.target_exercise is not None:
            return target_detection

        if not target_detection.ambiguous_matches:
            return target_detection

        resolved_target = resolve_target_from_clarification(
            intention,
            request.clarification_answers,
            target_detection.ambiguous_matches,
        )
        if resolved_target is None:
            return target_detection

        exercise_level = resolved_target.get("difficulty_level")
        target_above_group_level = (
            exercise_level in LEVEL_RANK
            and group_level in LEVEL_RANK
            and LEVEL_RANK[exercise_level] > LEVEL_RANK[group_level]
        )
        return TargetDetectionResult(
            target_exercise=resolved_target,
            target_above_group_level=target_above_group_level,
        )
