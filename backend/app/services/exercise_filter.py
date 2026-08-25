LEVEL_RANK = {
    "beginner": 0,
    "intermediate": 1,
    "advanced": 2,
}


def exercise_level_allowed(exercise_level: str, group_level: str) -> bool:
    return LEVEL_RANK[exercise_level] <= LEVEL_RANK[group_level]


def exercise_equipment_allowed(exercise: dict, group: dict) -> bool:
    possible_equipment = exercise.get("possible_equipment") or []
    if not possible_equipment:
        return True

    available_equipment = set(group.get("available_equipment") or [])
    return bool(available_equipment.intersection(possible_equipment))


def exercise_considerations_allowed(
    exercise_id: str,
    group_considerations: list[str],
    restrictions_by_exercise: dict[str, list[dict]],
) -> bool:
    if not group_considerations:
        return True

    restrictions = restrictions_by_exercise.get(exercise_id, [])
    group_consideration_set = set(group_considerations)

    for restriction in restrictions:
        if (
            restriction.get("compatibility") == "avoid"
            and restriction.get("restriction_key") in group_consideration_set
        ):
            return False

    return True


def filter_exercises(
    exercises: list[dict],
    group: dict,
    restrictions_by_exercise: dict[str, list[dict]] | None = None,
    check_level: bool = True,
) -> list[dict]:
    restrictions_by_exercise = restrictions_by_exercise or {}
    filtered = []

    for exercise in exercises:
        if check_level and not exercise_level_allowed(exercise["difficulty_level"], group["level"]):
            continue
        if not exercise_equipment_allowed(exercise, group):
            continue
        if not exercise_considerations_allowed(
            exercise["id"],
            group.get("group_considerations") or [],
            restrictions_by_exercise,
        ):
            continue
        filtered.append(exercise)

    return filtered


def find_unsuitable_exercise_ids(
    exercises: list[dict],
    group: dict,
    restrictions_by_exercise: dict[str, list[dict]] | None = None,
    check_level: bool = True,
) -> list[str]:
    suitable_ids = {
        exercise["id"]
        for exercise in filter_exercises(
            exercises,
            group,
            restrictions_by_exercise,
            check_level=check_level,
        )
    }
    return [exercise["id"] for exercise in exercises if exercise["id"] not in suitable_ids]
