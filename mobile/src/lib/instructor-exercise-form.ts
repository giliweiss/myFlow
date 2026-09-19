import { levelToApi, levelToDisplay, parseCommaList, formatCommaList } from './group-form';
import type {
  CreateInstructorExerciseInput,
  InstructorExercise,
  UpdateInstructorExerciseInput,
} from '../types/instructor-exercise';

export interface InstructorExerciseFormValues {
  nameHe: string;
  nameEn: string;
  descriptionHe: string;
  level: string;
  bodyFocus: string;
  equipment: string;
  teachingNotes: string;
}

export function instructorExerciseToFormValues(
  exercise: InstructorExercise,
): InstructorExerciseFormValues {
  return {
    nameHe: exercise.name_he,
    nameEn: exercise.name_en ?? '',
    descriptionHe: exercise.description_he ?? '',
    level: levelToDisplay(exercise.difficulty_level as 'beginner' | 'intermediate' | 'advanced'),
    bodyFocus: formatCommaList(exercise.body_focus),
    equipment: formatCommaList(exercise.possible_equipment),
    teachingNotes: exercise.teaching_notes ?? '',
  };
}

export function formValuesToCreateInput(
  values: InstructorExerciseFormValues,
): CreateInstructorExerciseInput {
  return {
    name_he: values.nameHe.trim(),
    name_en: values.nameEn.trim() || null,
    description_he: values.descriptionHe.trim() || null,
    difficulty_level: levelToApi(values.level),
    body_focus: parseCommaList(values.bodyFocus),
    possible_equipment: parseCommaList(values.equipment),
    teaching_notes: values.teachingNotes.trim() || null,
    source: 'manual',
  };
}

export function formValuesToUpdateInput(
  values: InstructorExerciseFormValues,
): UpdateInstructorExerciseInput {
  return {
    name_he: values.nameHe.trim(),
    name_en: values.nameEn.trim() || null,
    description_he: values.descriptionHe.trim() || null,
    difficulty_level: levelToApi(values.level),
    body_focus: parseCommaList(values.bodyFocus),
    possible_equipment: parseCommaList(values.equipment),
    teaching_notes: values.teachingNotes.trim() || null,
  };
}

export function filterInstructorExercisesBySearch<
  T extends { name_he: string; name_en?: string | null },
>(exercises: T[], searchText: string): T[] {
  const query = searchText.trim().toLowerCase();
  if (!query) {
    return exercises;
  }

  return exercises.filter((exercise) => {
    const searchableText = [exercise.name_he, exercise.name_en ?? '']
      .join(' ')
      .toLowerCase();
    return searchableText.includes(query);
  });
}
