-- Lessons and structured lesson exercises

CREATE TABLE public.lessons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  group_id uuid NOT NULL REFERENCES public.groups (id) ON DELETE CASCADE,
  title text NOT NULL,
  scheduled_for timestamptz,
  status text NOT NULL DEFAULT 'draft',
  primary_goal text,
  secondary_goals text[] NOT NULL DEFAULT '{}',
  level text NOT NULL,
  planned_duration_minutes integer,
  actual_duration_minutes integer,
  instructor_notes text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT lessons_status_check CHECK (
    status IN ('draft', 'planned', 'taught', 'cancelled')
  ),
  CONSTRAINT lessons_level_check CHECK (
    level IN ('beginner', 'intermediate', 'advanced')
  ),
  CONSTRAINT lessons_planned_duration_minutes_check CHECK (
    planned_duration_minutes IS NULL OR planned_duration_minutes > 0
  ),
  CONSTRAINT lessons_actual_duration_minutes_check CHECK (
    actual_duration_minutes IS NULL OR actual_duration_minutes > 0
  )
);

CREATE INDEX lessons_group_id_idx ON public.lessons (group_id);
CREATE INDEX lessons_status_idx ON public.lessons (status);
CREATE INDEX lessons_scheduled_for_idx ON public.lessons (scheduled_for);

CREATE TRIGGER lessons_set_updated_at
  BEFORE UPDATE ON public.lessons
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE public.lesson_exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid NOT NULL REFERENCES public.lessons (id) ON DELETE CASCADE,
  exercise_id uuid NOT NULL REFERENCES public.exercises (id) ON DELETE RESTRICT,
  order_index integer NOT NULL,
  section text NOT NULL,
  planned_duration_seconds integer,
  actual_duration_seconds integer,
  sets integer,
  reps integer,
  selected_modification text,
  instructor_notes text,
  completion_status text,

  CONSTRAINT lesson_exercises_section_check CHECK (
    section IN ('warmup', 'main', 'cooldown')
  ),
  CONSTRAINT lesson_exercises_completion_status_check CHECK (
    completion_status IS NULL
    OR completion_status IN ('completed', 'shortened', 'skipped')
  ),
  CONSTRAINT lesson_exercises_order_unique UNIQUE (lesson_id, order_index)
);

CREATE INDEX lesson_exercises_lesson_id_idx ON public.lesson_exercises (lesson_id);
CREATE INDEX lesson_exercises_exercise_id_idx ON public.lesson_exercises (exercise_id);

ALTER TABLE public.lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lesson_exercises ENABLE ROW LEVEL SECURITY;

CREATE POLICY lessons_select_own
  ON public.lessons
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.groups g
      WHERE g.id = group_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lessons_insert_own
  ON public.lessons
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1
      FROM public.groups g
      WHERE g.id = group_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lessons_update_own
  ON public.lessons
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.groups g
      WHERE g.id = group_id
        AND g.instructor_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1
      FROM public.groups g
      WHERE g.id = group_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lessons_delete_own
  ON public.lessons
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.groups g
      WHERE g.id = group_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lesson_exercises_select_own
  ON public.lesson_exercises
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.lessons l
      JOIN public.groups g ON g.id = l.group_id
      WHERE l.id = lesson_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lesson_exercises_insert_own
  ON public.lesson_exercises
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1
      FROM public.lessons l
      JOIN public.groups g ON g.id = l.group_id
      WHERE l.id = lesson_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lesson_exercises_update_own
  ON public.lesson_exercises
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.lessons l
      JOIN public.groups g ON g.id = l.group_id
      WHERE l.id = lesson_id
        AND g.instructor_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1
      FROM public.lessons l
      JOIN public.groups g ON g.id = l.group_id
      WHERE l.id = lesson_id
        AND g.instructor_id = auth.uid()
    )
  );

CREATE POLICY lesson_exercises_delete_own
  ON public.lesson_exercises
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM public.lessons l
      JOIN public.groups g ON g.id = l.group_id
      WHERE l.id = lesson_id
        AND g.instructor_id = auth.uid()
    )
  );
