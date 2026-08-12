from app.core.config import settings
from app.repositories.exercise_repo import ExerciseRepository
from app.repositories.group_member_repo import GroupMemberRepository
from app.repositories.group_repo import GroupRepository
from app.repositories.instructor_profile_repo import InstructorProfileRepository
from app.repositories.lesson_attendance_repo import LessonAttendanceRepository
from app.repositories.lesson_exercise_repo import LessonExerciseRepository
from app.repositories.lesson_repo import LessonRepository
from app.repositories.review_repo import ReviewRepository
from app.services.attendance_service import AttendanceService


def get_supabase_client():
    from supabase import create_client

    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_exercise_repository() -> ExerciseRepository:
    return ExerciseRepository(get_supabase_client())


def get_group_repository() -> GroupRepository:
    return GroupRepository(get_supabase_client())


def get_instructor_profile_repository() -> InstructorProfileRepository:
    return InstructorProfileRepository(get_supabase_client())


def get_group_member_repository() -> GroupMemberRepository:
    return GroupMemberRepository(get_supabase_client())


def get_lesson_repository() -> LessonRepository:
    return LessonRepository(get_supabase_client())


def get_lesson_exercise_repository() -> LessonExerciseRepository:
    return LessonExerciseRepository(get_supabase_client())


def get_lesson_attendance_repository() -> LessonAttendanceRepository:
    return LessonAttendanceRepository(get_supabase_client())


def get_review_repository() -> ReviewRepository:
    return ReviewRepository(get_supabase_client())


def get_attendance_service() -> AttendanceService:
    return AttendanceService(
        get_lesson_repository(),
        get_group_member_repository(),
        get_lesson_attendance_repository(),
    )
