-- Exercise knowledge-base catalog (shared read-only for authenticated users)

-- ---------------------------------------------------------------------------
-- Helper: keep exercises.updated_at in sync
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = timezone('utc', now());
  RETURN NEW;
END;
$$;

-- ---------------------------------------------------------------------------
-- exercises
-- ---------------------------------------------------------------------------
CREATE TABLE public.exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_key text NOT NULL,
  name_en text NOT NULL,
  name_he text NOT NULL,
  description_en text,
  description_he text,
  difficulty_level text NOT NULL,
  body_focus text[] NOT NULL DEFAULT '{}',
  position text,
  possible_equipment text[] NOT NULL DEFAULT '{}',
  intensity integer,
  min_duration_seconds integer,
  max_duration_seconds integer,
  min_reps integer,
  max_reps integer,
  phase_affinities text[] NOT NULL DEFAULT '{}',
  teaching_cues_en text[] NOT NULL DEFAULT '{}',
  teaching_cues_he text[] NOT NULL DEFAULT '{}',
  common_mistakes_en text[] NOT NULL DEFAULT '{}',
  common_mistakes_he text[] NOT NULL DEFAULT '{}',
  aliases_en text[] NOT NULL DEFAULT '{}',
  aliases_he text[] NOT NULL DEFAULT '{}',
  pilates_principles text[] NOT NULL DEFAULT '{}',
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT exercises_canonical_key_unique UNIQUE (canonical_key),
  CONSTRAINT exercises_difficulty_level_check CHECK (
    difficulty_level IN ('beginner', 'intermediate', 'advanced')
  ),
  CONSTRAINT exercises_intensity_check CHECK (
    intensity IS NULL OR (intensity >= 1 AND intensity <= 5)
  ),
  CONSTRAINT exercises_duration_range_check CHECK (
    min_duration_seconds IS NULL
    OR max_duration_seconds IS NULL
    OR min_duration_seconds <= max_duration_seconds
  ),
  CONSTRAINT exercises_reps_range_check CHECK (
    min_reps IS NULL
    OR max_reps IS NULL
    OR min_reps <= max_reps
  )
);

CREATE INDEX exercises_is_active_idx ON public.exercises (is_active);
CREATE INDEX exercises_difficulty_level_idx ON public.exercises (difficulty_level);
CREATE INDEX exercises_position_idx ON public.exercises (position);
CREATE INDEX exercises_name_en_idx ON public.exercises (name_en);

CREATE TRIGGER exercises_set_updated_at
  BEFORE UPDATE ON public.exercises
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

-- ---------------------------------------------------------------------------
-- exercise_restrictions
-- ---------------------------------------------------------------------------
CREATE TABLE public.exercise_restrictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  exercise_id uuid NOT NULL REFERENCES public.exercises (id) ON DELETE CASCADE,
  restriction_key text NOT NULL,
  compatibility text NOT NULL,
  modification_notes_en text,
  modification_notes_he text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT exercise_restrictions_compatibility_check CHECK (
    compatibility IN ('allowed', 'modify', 'avoid')
  ),
  CONSTRAINT exercise_restrictions_exercise_restriction_unique UNIQUE (
    exercise_id,
    restriction_key
  )
);

CREATE INDEX exercise_restrictions_exercise_id_idx
  ON public.exercise_restrictions (exercise_id);

CREATE INDEX exercise_restrictions_restriction_key_idx
  ON public.exercise_restrictions (restriction_key);

-- ---------------------------------------------------------------------------
-- exercise_relations
-- ---------------------------------------------------------------------------
CREATE TABLE public.exercise_relations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  exercise_id uuid NOT NULL REFERENCES public.exercises (id) ON DELETE CASCADE,
  related_exercise_id uuid NOT NULL REFERENCES public.exercises (id) ON DELETE CASCADE,
  relation_type text NOT NULL,
  notes text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT exercise_relations_relation_type_check CHECK (
    relation_type IN ('regression', 'progression', 'alternative')
  ),
  CONSTRAINT exercise_relations_no_self_relation_check CHECK (
    exercise_id <> related_exercise_id
  ),
  CONSTRAINT exercise_relations_unique_relation UNIQUE (
    exercise_id,
    related_exercise_id,
    relation_type
  )
);

CREATE INDEX exercise_relations_exercise_id_idx
  ON public.exercise_relations (exercise_id);

CREATE INDEX exercise_relations_related_exercise_id_idx
  ON public.exercise_relations (related_exercise_id);

CREATE INDEX exercise_relations_relation_type_idx
  ON public.exercise_relations (relation_type);

-- ---------------------------------------------------------------------------
-- Row Level Security: shared catalog, read-only for authenticated users
-- ---------------------------------------------------------------------------
ALTER TABLE public.exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_restrictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_relations ENABLE ROW LEVEL SECURITY;

CREATE POLICY exercises_select_authenticated
  ON public.exercises
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY exercise_restrictions_select_authenticated
  ON public.exercise_restrictions
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY exercise_relations_select_authenticated
  ON public.exercise_relations
  FOR SELECT
  TO authenticated
  USING (true);
