export type LessonSection = 'warmup' | 'main' | 'cooldown';

export type LessonStatus = 'upcoming' | 'completed' | 'cancelled';

export interface BuilderExercise {
  localId: string;
  exerciseId: string;
  nameHe: string;
  section: LessonSection;
}

export interface LessonExerciseInput {
  exercise_id: string;
  order_index: number;
  section: LessonSection;
  planned_duration_seconds?: number;
  sets?: number;
  reps?: number;
  selected_modification?: string;
  instructor_notes?: string;
}

export interface CreateLessonInput {
  title: string;
  primary_goal?: string;
  secondary_goals?: string[];
  instructor_notes?: string;
  planned_duration_minutes?: number;
  scheduled_for?: string;
  lesson_exercises: LessonExerciseInput[];
}

export interface UpdateLessonInput {
  title?: string;
  status?: LessonStatus;
  scheduled_for?: string | null;
  primary_goal?: string | null;
  instructor_notes?: string | null;
  planned_duration_minutes?: number;
  lesson_exercises?: LessonExerciseInput[];
}

export interface LessonSummary {
  id: string;
  group_id: string;
  title: string;
  status: LessonStatus;
  scheduled_for: string | null;
  planned_duration_minutes: number | null;
  created_at: string;
  updated_at: string;
  has_review: boolean;
}

export interface LessonExercise {
  id: string;
  lesson_id: string;
  exercise_id: string;
  order_index: number;
  section: LessonSection;
  planned_duration_seconds: number | null;
  actual_duration_seconds: number | null;
  sets: number | null;
  reps: number | null;
  selected_modification: string | null;
  instructor_notes: string | null;
  completion_status: string | null;
}

export interface Lesson {
  id: string;
  group_id: string;
  title: string;
  status: LessonStatus;
  scheduled_for: string | null;
  primary_goal: string | null;
  secondary_goals: string[];
  level: string;
  planned_duration_minutes: number | null;
  actual_duration_minutes: number | null;
  instructor_notes: string | null;
  created_at: string;
  updated_at: string;
  lesson_exercises: LessonExercise[];
}
