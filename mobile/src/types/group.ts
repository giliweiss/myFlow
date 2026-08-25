export type GroupLevel = 'beginner' | 'intermediate' | 'advanced';

export interface Group {
  id: string;
  instructor_id: string;
  name: string;
  level: GroupLevel;
  studio_name: string | null;
  location_notes: string | null;
  weekday: number | null;
  start_time: string | null;
  typical_duration_minutes: number;
  available_equipment: string[];
  group_considerations: string[];
  notes: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UpdateGroupInput {
  name?: string;
  level?: GroupLevel;
  typical_duration_minutes?: number;
  available_equipment?: string[];
  group_considerations?: string[];
  notes?: string | null;
}
