# LLM service (to be implemented in Phase 3)
# Generates lessons using Claude or GPT-4o


class LessonGeneratorProtocol:
    """Protocol for LLM-based lesson generation."""

    def generate(self, context: dict) -> dict:
        """
        Generate a lesson plan from group context.

        Context includes:
        - group level, duration, equipment, considerations
        - recent exercises (to avoid repetition)
        - goals
        """
        raise NotImplementedError("To be implemented in Phase 3")
