-- Instructor identity and groups (Phase 1)

-- ---------------------------------------------------------------------------
-- instructor_profiles
-- ---------------------------------------------------------------------------
CREATE TABLE public.instructor_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users (id) ON DELETE CASCADE,
  display_name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);

CREATE TRIGGER instructor_profiles_set_updated_at
  BEFORE UPDATE ON public.instructor_profiles
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

-- ---------------------------------------------------------------------------
-- groups
-- ---------------------------------------------------------------------------
CREATE TABLE public.groups (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  instructor_id uuid NOT NULL REFERENCES public.instructor_profiles (id) ON DELETE CASCADE,
  name text NOT NULL,
  level text NOT NULL,
  studio_name text,
  location_notes text,
  weekday smallint,
  start_time time,
  typical_duration_minutes integer NOT NULL DEFAULT 60,
  goals text[] NOT NULL DEFAULT '{}',
  available_equipment text[] NOT NULL DEFAULT '{}',
  group_considerations text[] NOT NULL DEFAULT '{}',
  notes text,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT groups_level_check CHECK (
    level IN ('beginner', 'intermediate', 'advanced')
  ),
  CONSTRAINT groups_weekday_check CHECK (
    weekday IS NULL OR (weekday >= 0 AND weekday <= 6)
  ),
  CONSTRAINT groups_typical_duration_minutes_check CHECK (
    typical_duration_minutes > 0
  )
);

CREATE INDEX groups_instructor_id_idx ON public.groups (instructor_id);
CREATE INDEX groups_is_active_idx ON public.groups (is_active);
CREATE INDEX groups_schedule_idx ON public.groups (weekday, start_time);

CREATE TRIGGER groups_set_updated_at
  BEFORE UPDATE ON public.groups
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

-- ---------------------------------------------------------------------------
-- Row Level Security
-- ---------------------------------------------------------------------------
ALTER TABLE public.instructor_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.groups ENABLE ROW LEVEL SECURITY;

CREATE POLICY instructor_profiles_select_own
  ON public.instructor_profiles
  FOR SELECT
  TO authenticated
  USING (id = auth.uid());

CREATE POLICY instructor_profiles_insert_own
  ON public.instructor_profiles
  FOR INSERT
  TO authenticated
  WITH CHECK (id = auth.uid());

CREATE POLICY instructor_profiles_update_own
  ON public.instructor_profiles
  FOR UPDATE
  TO authenticated
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

CREATE POLICY groups_select_own
  ON public.groups
  FOR SELECT
  TO authenticated
  USING (instructor_id = auth.uid());

CREATE POLICY groups_insert_own
  ON public.groups
  FOR INSERT
  TO authenticated
  WITH CHECK (instructor_id = auth.uid());

CREATE POLICY groups_update_own
  ON public.groups
  FOR UPDATE
  TO authenticated
  USING (instructor_id = auth.uid())
  WITH CHECK (instructor_id = auth.uid());

CREATE POLICY groups_delete_own
  ON public.groups
  FOR DELETE
  TO authenticated
  USING (instructor_id = auth.uid());
