export type InstructorExerciseSource = 'manual' | 'ai_saved';

export interface InstructorExercise {
  id: string;
  instructor_id: string;
  name_he: string;
  name_en: string | null;
  description_he: string | null;
  difficulty_level: string;
  body_focus: string[];
  possible_equipment: string[];
  teaching_notes: string | null;
  source: InstructorExerciseSource;
  based_on_catalog_exercise_id: string | null;
  based_on_modification: string | null;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateInstructorExerciseInput {
  name_he: string;
  name_en?: string | null;
  description_he?: string | null;
  difficulty_level: string;
  body_focus?: string[];
  possible_equipment?: string[];
  teaching_notes?: string | null;
  source?: InstructorExerciseSource;
  based_on_catalog_exercise_id?: string | null;
  based_on_modification?: string | null;
}

export interface UpdateInstructorExerciseInput {
  name_he?: string;
  name_en?: string | null;
  description_he?: string | null;
  difficulty_level?: string;
  body_focus?: string[];
  possible_equipment?: string[];
  teaching_notes?: string | null;
  is_archived?: boolean;
}
