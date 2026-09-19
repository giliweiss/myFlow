from dataclasses import dataclass, field


@dataclass
class LessonPlanningContext:
    intention: str
    preparation_catalog: list[dict]
    target_exercise: dict | None = None
    target_above_group_level: bool = False
    target_relations: list[dict] = field(default_factory=list)
