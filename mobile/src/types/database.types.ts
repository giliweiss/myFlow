// Auto-generated from Supabase schema (Phase 1)
// Placeholder for now

export type Database = {
  public: {
    Tables: {
      instructor_profiles: {
        Row: {
          id: string;
          display_name: string;
          created_at: string;
          updated_at: string;
        };
      };
      groups: {
        Row: {
          id: string;
          instructor_id: string;
          name: string;
          level: 'beginner' | 'intermediate' | 'advanced';
          studio_name: string | null;
          location_notes: string | null;
          weekday: string | null;
          start_time: string | null;
          typical_duration_minutes: number;
          available_equipment: string[];
          group_considerations: string[];
          notes: string | null;
          is_active: boolean;
          created_at: string;
          updated_at: string;
        };
      };
      // ... more tables
    };
  };
};
