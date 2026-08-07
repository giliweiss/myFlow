# Lesson validation service (deterministic)
# Validates: duration, sections, exercise IDs


def validate_lesson(lesson_data: dict) -> dict:
    """
    Validate lesson structure and duration.

    - Total duration within ±10% of requested
    - Sections: warmup ~15%, main ~70%, cooldown ~15%
    - All exercise IDs exist
    """
    # To be implemented in Phase 1
    return {"valid": True, "issues": []}
