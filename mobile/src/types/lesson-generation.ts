import type { LessonSection } from './lesson';

export interface ClarificationAnswer {
  question_id: string;
  answer: string;
}

export interface GenerateLessonRequest {
  intention?: string | null;
  planned_duration_minutes?: number;
  notes?: string | null;
  clarification_answers?: ClarificationAnswer[];
  primary_goal?: string | null;
  secondary_goals?: string[];
}

export interface ClarificationQuestion {
  question_id: string;
  prompt: string;
  why_needed?: string | null;
}

export interface GeneratedExerciseAlternative {
  exercise_id: string;
  relation_type: 'alternative' | 'regression' | 'progression';
  reason?: string | null;
}

export interface GeneratedLessonExercise {
  exercise_id: string;
  order_index: number;
  section: LessonSection;
  planned_duration_seconds?: number | null;
  sets?: number | null;
  reps?: number | null;
  selected_modification?: string | null;
  instructor_notes?: string | null;
  alternatives?: GeneratedExerciseAlternative[];
}

export interface GeneratedExerciseGuidance {
  exercise_id: string;
  why_chosen?: string | null;
  progression_role?: string | null;
  teaching_cues?: string[];
  creative_variations?: string[];
}

export interface GeneratedLessonGuidance {
  lesson_strategy?: string | null;
  structure_rationale?: string | null;
  progression_logic?: string | null;
  section_notes?: Record<string, string>;
  exercise_guidance?: GeneratedExerciseGuidance[];
}

export interface GenerateLessonClarificationResponse {
  status: 'needs_clarification';
  group_id: string;
  clarification_questions: ClarificationQuestion[];
}

export interface GenerateLessonReadyResponse {
  status: 'ready';
  group_id: string;
  title: string;
  primary_goal: string;
  secondary_goals: string[];
  planned_duration_minutes: number;
  instructor_notes?: string | null;
  lesson_exercises: GeneratedLessonExercise[];
  guidance: GeneratedLessonGuidance;
}

export type GenerateLessonResponse =
  | GenerateLessonClarificationResponse
  | GenerateLessonReadyResponse;

export function isReadyLessonResponse(
  response: GenerateLessonResponse,
): response is GenerateLessonReadyResponse {
  return response.status === 'ready';
}

export function isClarificationResponse(
  response: GenerateLessonResponse,
): response is GenerateLessonClarificationResponse {
  return response.status === 'needs_clarification';
}

/** @deprecated Use GenerateLessonReadyResponse */
export type GeneratedLessonResponse = GenerateLessonReadyResponse;
