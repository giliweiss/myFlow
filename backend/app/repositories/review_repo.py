"""Repository for Lesson Review data access."""

from app.repositories.base_repo import BaseRepository


class ReviewRepository(BaseRepository):
    """Repository for managing lesson reviews."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lesson_reviews")

    async def get_recent_by_group(self, group_id: str, limit: int = 10):
        """Get recent reviews for a group."""
        # Stub: query reviews for group's lessons, ordered desc
        return []

    async def create(self, lesson_id: str, review_data: dict):
        """Create a lesson review."""
        review_data["lesson_id"] = lesson_id
        # Stub: insert into Supabase
        return review_data
