import type { Exercise } from '../types/exercise';
import type { GroupLevel } from '../types/group';
import { strings } from '../i18n/he';
import type {
  BuilderExercise,
  CreateLessonInput,
  Lesson,
  LessonExercise,
  LessonExerciseInput,
  LessonSection,
  LessonStatus,
  UpdateLessonInput,
} from '../types/lesson';

export const LESSON_SECTIONS: LessonSection[] = ['warmup', 'main', 'cooldown'];

export function createLocalId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function createBuilderExercise(
  exercise: Exercise,
  section: LessonSection,
): BuilderExercise {
  return {
    localId: createLocalId(),
    exerciseId: exercise.id,
    nameHe: exercise.name_he,
    section,
  };
}

export function addExerciseToSection(
  exercises: BuilderExercise[],
  exercise: Exercise,
  section: LessonSection,
): BuilderExercise[] {
  return [...exercises, createBuilderExercise(exercise, section)];
}

export function removeBuilderExercise(
  exercises: BuilderExercise[],
  localId: string,
): BuilderExercise[] {
  return exercises.filter((item) => item.localId !== localId);
}

export function moveExerciseInSection(
  exercises: BuilderExercise[],
  localId: string,
  direction: 'up' | 'down',
): BuilderExercise[] {
  const index = exercises.findIndex((item) => item.localId === localId);
  if (index === -1) {
    return exercises;
  }

  const section = exercises[index].section;
  const sectionIndexes = exercises
    .map((item, itemIndex) => ({ item, itemIndex }))
    .filter(({ item }) => item.section === section)
    .map(({ itemIndex }) => itemIndex);

  const sectionPosition = sectionIndexes.indexOf(index);
  if (sectionPosition === -1) {
    return exercises;
  }

  const targetSectionPosition =
    direction === 'up' ? sectionPosition - 1 : sectionPosition + 1;

  if (targetSectionPosition < 0 || targetSectionPosition >= sectionIndexes.length) {
    return exercises;
  }

  const targetIndex = sectionIndexes[targetSectionPosition];
  const nextExercises = [...exercises];
  [nextExercises[index], nextExercises[targetIndex]] = [
    nextExercises[targetIndex],
    nextExercises[index],
  ];
  return nextExercises;
}

export function builderExercisesToInput(
  exercises: BuilderExercise[],
): LessonExerciseInput[] {
  return exercises.map((exercise, index) => ({
    exercise_id: exercise.exerciseId,
    order_index: index,
    section: exercise.section,
  }));
}

export function buildCreateLessonInput(params: {
  title: string;
  primaryGoal: string;
  notes: string;
  plannedDurationMinutes: number;
  scheduledDate: string;
  exercises: BuilderExercise[];
}): CreateLessonInput {
  const input: CreateLessonInput = {
    title: params.title.trim(),
    planned_duration_minutes: params.plannedDurationMinutes,
    lesson_exercises: builderExercisesToInput(params.exercises),
  };

  const primaryGoal = params.primaryGoal.trim();
  if (primaryGoal) {
    input.primary_goal = primaryGoal;
  }

  const notes = params.notes.trim();
  if (notes) {
    input.instructor_notes = notes;
  }

  const scheduledFor = parseDateInputToIso(params.scheduledDate);
  if (scheduledFor) {
    input.scheduled_for = scheduledFor;
  }

  return input;
}

export function buildUpdateLessonInput(params: {
  title: string;
  primaryGoal: string;
  notes: string;
  plannedDurationMinutes: number;
  scheduledDate: string;
  status: LessonStatus;
  exercises: BuilderExercise[];
}): UpdateLessonInput {
  const input: UpdateLessonInput = {
    title: params.title.trim(),
    status: params.status,
    planned_duration_minutes: params.plannedDurationMinutes,
    lesson_exercises: builderExercisesToInput(params.exercises),
    primary_goal: params.primaryGoal.trim() || null,
    instructor_notes: params.notes.trim() || null,
  };

  const scheduledFor = parseDateInputToIso(params.scheduledDate);
  input.scheduled_for = scheduledFor;

  return input;
}

export function todayDateInput(): string {
  return formatIsoToDateInput(new Date().toISOString());
}

export function formatIsoToDateInput(iso: string | null | undefined): string {
  if (!iso) {
    return '';
  }

  const date = new Date(iso);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}

export function parseDateInputToIso(dateText: string): string | null {
  const trimmed = dateText.trim();
  const match = trimmed.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!match) {
    return null;
  }

  const day = Number(match[1]);
  const month = Number(match[2]);
  const year = Number(match[3]);
  const date = new Date(year, month - 1, day, 12, 0, 0);

  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return null;
  }

  return date.toISOString();
}

export function formatLessonDateDisplay(
  scheduledFor: string | null | undefined,
  fallbackIso?: string | null,
): string {
  const value = scheduledFor ?? fallbackIso;
  if (!value) {
    return strings.lessons.noDate;
  }

  return new Date(value).toLocaleDateString('he-IL', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export function lessonExercisesToBuilder(
  lessonExercises: LessonExercise[],
  catalogExercises: Exercise[],
): BuilderExercise[] {
  const catalogById = new Map(
    catalogExercises.map((exercise) => [exercise.id, exercise]),
  );

  return [...lessonExercises]
    .sort((left, right) => left.order_index - right.order_index)
    .map((item) => ({
      localId: item.id,
      exerciseId: item.exercise_id,
      nameHe: catalogById.get(item.exercise_id)?.name_he ?? item.exercise_id,
      section: item.section,
    }));
}

export function lessonToFormState(
  lesson: Lesson,
  catalogExercises: Exercise[],
): {
  title: string;
  primaryGoal: string;
  notes: string;
  duration: string;
  scheduledDate: string;
  status: LessonStatus;
  exercises: BuilderExercise[];
} {
  return {
    title: lesson.title,
    primaryGoal: lesson.primary_goal ?? '',
    notes: lesson.instructor_notes ?? '',
    duration: String(lesson.planned_duration_minutes ?? ''),
    scheduledDate:
      formatIsoToDateInput(lesson.scheduled_for) || todayDateInput(),
    status: lesson.status,
    exercises: lessonExercisesToBuilder(lesson.lesson_exercises, catalogExercises),
  };
}

export function filterExercisesBySearch(
  exercises: Exercise[],
  searchText: string,
): Exercise[] {
  const query = searchText.trim().toLowerCase();
  if (!query) {
    return exercises;
  }

  return exercises.filter((exercise) => {
    const searchableText = [
      exercise.name_he,
      exercise.name_en,
      ...exercise.aliases_he,
      ...exercise.aliases_en,
    ]
      .join(' ')
      .toLowerCase();

    return searchableText.includes(query);
  });
}

export function findExercisesWithLevelMismatch(
  builderExercises: BuilderExercise[],
  catalogExercises: Exercise[],
  groupLevel: GroupLevel,
): string[] {
  const catalogById = new Map(
    catalogExercises.map((exercise) => [exercise.id, exercise]),
  );

  const mismatchNames: string[] = [];

  for (const builderExercise of builderExercises) {
    const catalogExercise = catalogById.get(builderExercise.exerciseId);
    if (
      catalogExercise &&
      catalogExercise.difficulty_level !== groupLevel
    ) {
      mismatchNames.push(builderExercise.nameHe);
    }
  }

  return mismatchNames;
}
