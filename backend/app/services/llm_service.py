from typing import Protocol

from app.schemas.lesson_generation import GenerateLessonRequest
from app.schemas.llm_lesson_plan import LLMClarificationOutput, LLMPlanningOutput
from app.services.clarification_rules import ForcedClarification
from app.services.lesson_planning_context import LessonPlanningContext


class LessonGenerationLLM(Protocol):
    def formulate_clarification_questions(
        self,
        group: dict,
        request: GenerateLessonRequest,
        forced_clarifications: list[ForcedClarification],
    ) -> LLMClarificationOutput:
        ...

    def generate_lesson_plan(
        self,
        group: dict,
        request: GenerateLessonRequest,
        planning_context: LessonPlanningContext,
    ) -> LLMPlanningOutput:
        ...
