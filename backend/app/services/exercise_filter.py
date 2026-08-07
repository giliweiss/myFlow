# Exercise filtering service (deterministic, no LLM)
# Filters exercises by: level, equipment, considerations/restrictions


def filter_exercises(exercises: list, group_context: dict) -> list:
    """
    Filter exercises by group constraints.

    - level: min_level <= group.level <= max_level
    - equipment: group.available_equipment covers exercise.equipment_required
    - considerations: avoid exercises with matching contraindications
    """
    # To be implemented in Phase 1
    return exercises
