import type { BuilderExercise } from '../types/lesson';
import type { GeneratedLessonGuidance } from '../types/lesson-generation';

export interface LessonBuilderDraft {
  title: string;
  primaryGoal: string;
  notes: string;
  plannedDurationMinutes: number;
  exercises: BuilderExercise[];
}

export interface LessonPlanReviewDraft {
  groupId: string;
  intention: string;
  duration: string;
  notes: string;
  title: string;
  primaryGoal: string;
  plannedDurationMinutes: number;
  instructorNotes: string;
  guidance: GeneratedLessonGuidance;
  builderDraft: LessonBuilderDraft;
}

let pendingBuilderDraft: LessonBuilderDraft | null = null;
let pendingPlanReviewDraft: LessonPlanReviewDraft | null = null;

export function setLessonBuilderDraft(draft: LessonBuilderDraft): void {
  pendingBuilderDraft = draft;
}

export function consumeLessonBuilderDraft(): LessonBuilderDraft | null {
  const draft = pendingBuilderDraft;
  pendingBuilderDraft = null;
  return draft;
}

export function setLessonPlanReviewDraft(draft: LessonPlanReviewDraft): void {
  pendingPlanReviewDraft = draft;
}

export function consumeLessonPlanReviewDraft(): LessonPlanReviewDraft | null {
  const draft = pendingPlanReviewDraft;
  pendingPlanReviewDraft = null;
  return draft;
}
