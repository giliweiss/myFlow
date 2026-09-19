-- Instructor-owned custom exercises (separate from canonical catalog)

CREATE TABLE public.instructor_exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  instructor_id uuid NOT NULL REFERENCES public.instructor_profiles (id) ON DELETE CASCADE,
  name_he text NOT NULL,
  name_en text,
  description_he text,
  difficulty_level text NOT NULL,
  body_focus text[] NOT NULL DEFAULT '{}',
  possible_equipment text[] NOT NULL DEFAULT '{}',
  teaching_notes text,
  source text NOT NULL DEFAULT 'manual',
  based_on_catalog_exercise_id uuid REFERENCES public.exercises (id) ON DELETE SET NULL,
  based_on_modification text,
  is_archived boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT instructor_exercises_difficulty_level_check CHECK (
    difficulty_level IN ('beginner', 'intermediate', 'advanced')
  ),
  CONSTRAINT instructor_exercises_source_check CHECK (
    source IN ('manual', 'ai_saved')
  )
);

CREATE INDEX instructor_exercises_instructor_id_idx
  ON public.instructor_exercises (instructor_id);

CREATE INDEX instructor_exercises_is_archived_idx
  ON public.instructor_exercises (is_archived);

CREATE TRIGGER instructor_exercises_set_updated_at
  BEFORE UPDATE ON public.instructor_exercises
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

ALTER TABLE public.instructor_exercises ENABLE ROW LEVEL SECURITY;

CREATE POLICY instructor_exercises_select_own
  ON public.instructor_exercises
  FOR SELECT
  TO authenticated
  USING (instructor_id = auth.uid());

CREATE POLICY instructor_exercises_insert_own
  ON public.instructor_exercises
  FOR INSERT
  TO authenticated
  WITH CHECK (instructor_id = auth.uid());

CREATE POLICY instructor_exercises_update_own
  ON public.instructor_exercises
  FOR UPDATE
  TO authenticated
  USING (instructor_id = auth.uid())
  WITH CHECK (instructor_id = auth.uid());

CREATE POLICY instructor_exercises_delete_own
  ON public.instructor_exercises
  FOR DELETE
  TO authenticated
  USING (instructor_id = auth.uid());
