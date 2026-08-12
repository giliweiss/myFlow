VALID_SECTIONS = {"warmup", "main", "cooldown"}

ALLOWED_STATUS_TRANSITIONS = {
    "draft": {"planned", "cancelled"},
    "planned": {"taught", "cancelled"},
    "taught": set(),
    "cancelled": set(),
}


def validate_exercise_items(exercise_items: list[dict]) -> dict:
    issues = []

    if not exercise_items:
        return {"valid": True, "issues": issues}

    order_indexes = [item["order_index"] for item in exercise_items]
    if len(order_indexes) != len(set(order_indexes)):
        issues.append("order_index values must be unique within the lesson")

    for item in exercise_items:
        if item.get("section") not in VALID_SECTIONS:
            issues.append(f"Invalid section: {item.get('section')}")

    return {"valid": len(issues) == 0, "issues": issues}


def validate_lesson_for_save(
    lesson_data: dict,
    exercise_items: list[dict],
    existing_exercise_ids: set[str],
) -> dict:
    issues = []

    structure_result = validate_exercise_items(exercise_items)
    issues.extend(structure_result["issues"])

    for item in exercise_items:
        if item["exercise_id"] not in existing_exercise_ids:
            issues.append(f"Unknown exercise_id: {item['exercise_id']}")

    planned_duration = lesson_data.get("planned_duration_minutes")
    if planned_duration is not None and planned_duration <= 0:
        issues.append("planned_duration_minutes must be greater than 0")

    return {"valid": len(issues) == 0, "issues": issues}


def validate_lesson_for_plan(
    lesson_data: dict,
    exercise_items: list[dict],
    existing_exercise_ids: set[str],
) -> dict:
    save_result = validate_lesson_for_save(lesson_data, exercise_items, existing_exercise_ids)
    issues = list(save_result["issues"])

    if not exercise_items:
        issues.append("At least one exercise is required to plan a lesson")

    if not lesson_data.get("title"):
        issues.append("title is required to plan a lesson")

    return {"valid": len(issues) == 0, "issues": issues}


def validate_status_transition(current_status: str, new_status: str) -> dict:
    if current_status == new_status:
        return {"valid": True, "issues": []}

    allowed = ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
    if new_status not in allowed:
        return {
            "valid": False,
            "issues": [f"Cannot transition from {current_status} to {new_status}"],
        }

    return {"valid": True, "issues": []}
