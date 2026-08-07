"""Repository for Lesson data access."""

from app.repositories.base_repo import BaseRepository


class LessonRepository(BaseRepository):
    """Repository for managing lessons."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lessons")

    async def get_by_id(self, lesson_id: str):
        """Get a lesson by ID."""
        # Stub: fetch from Supabase including lesson_exercises
        return None

    async def list_by_group(self, group_id: str, limit: int = 50):
        """List lessons for a group."""
        # Stub: query WHERE group_id = group_id, ordered by date
        return []

    async def get_recent_history(self, group_id: str, limit: int = 10):
        """Get recent taught lessons for a group."""
        # Stub: query WHERE group_id AND status = 'taught', limit, desc order
        return []

    async def create_draft(self, group_id: str, lesson_data: dict):
        """Create a lesson as draft with exercises."""
        lesson_data["group_id"] = group_id
        lesson_data["status"] = "draft"
        # Stub: insert lesson + lesson_exercises
        return lesson_data

    async def update_status(self, lesson_id: str, status: str):
        """Update lesson status (draft -> planned -> taught -> cancelled)."""
        # Stub: update status in Supabase
        return {"lesson_id": lesson_id, "status": status}

    async def add_exercises(self, lesson_id: str, exercises: list):
        """Add exercises to a lesson."""
        # Stub: insert into lesson_exercises
        pass
