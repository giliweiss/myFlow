from app.repositories.group_member_repo import GroupMemberRepository
from app.repositories.lesson_attendance_repo import LessonAttendanceRepository
from app.repositories.lesson_repo import LessonRepository


class AttendanceService:
    def __init__(
        self,
        lesson_repository: LessonRepository,
        group_member_repository: GroupMemberRepository,
        lesson_attendance_repository: LessonAttendanceRepository,
    ):
        self.lesson_repository = lesson_repository
        self.group_member_repository = group_member_repository
        self.lesson_attendance_repository = lesson_attendance_repository

    def seed_attendance_for_lesson(self, lesson_id: str, group_id: str) -> None:
        active_members = self.group_member_repository.list_active_by_group(group_id)
        member_ids = [member["id"] for member in active_members]
        self.lesson_attendance_repository.create_rows_for_members(lesson_id, member_ids)

    def add_attendance_for_new_member(self, group_id: str, member_id: str) -> None:
        upcoming_lessons = self.lesson_repository.list_by_group_and_status(group_id, "upcoming")
        for lesson in upcoming_lessons:
            self.lesson_attendance_repository.create_row_if_missing(lesson["id"], member_id)
