export interface Exercise {
  id: string;
  canonical_key: string;
  name_en: string;
  name_he: string;
  description_en: string | null;
  description_he: string | null;
  difficulty_level: string;
  body_focus: string[];
  position: string | null;
  possible_equipment: string[];
  intensity: number | null;
  min_duration_seconds: number | null;
  max_duration_seconds: number | null;
  min_reps: number | null;
  max_reps: number | null;
  phase_affinities: string[];
  teaching_cues_en: string[];
  teaching_cues_he: string[];
  common_mistakes_en: string[];
  common_mistakes_he: string[];
  aliases_en: string[];
  aliases_he: string[];
  pilates_principles: string[];
  is_active: boolean;
}
