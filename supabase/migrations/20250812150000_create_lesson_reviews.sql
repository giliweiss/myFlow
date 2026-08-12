-- Post-lesson reviews (one per lesson)

CREATE TABLE public.lesson_reviews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid NOT NULL REFERENCES public.lessons (id) ON DELETE CASCADE,
  perceived_difficulty integer NOT NULL,
  group_response text NOT NULL,
  goals_achieved text[] NOT NULL DEFAULT '{}',
  issues text[] NOT NULL DEFAULT '{}',
  instructor_notes text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),

  CONSTRAINT lesson_reviews_lesson_id_unique UNIQUE (lesson_id),
  CONSTRAINT lesson_reviews_perceived_difficulty_check CHECK (
    perceived_difficulty >= 1 AND perceived_difficulty <= 5
  ),
  CONSTRAINT lesson_reviews_group_response_check CHECK (
    group_response IN ('too_easy', 'appropriate', 'too_hard', 'mixed')
  )
);

CREATE INDEX lesson_reviews_lesson_id_idx ON public.lesson_reviews (lesson_id);

CREATE TRIGGER lesson_reviews_set_updated_at
  BEFORE UPDATE ON public.lesson_reviews
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

ALTER TABLE public.lesson_reviews ENABLE ROW LEVEL SECURITY;

CREATE POLICY lesson_reviews_select_own
  ON public.lesson_reviews
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

CREATE POLICY lesson_reviews_insert_own
  ON public.lesson_reviews
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

CREATE POLICY lesson_reviews_update_own
  ON public.lesson_reviews
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

CREATE POLICY lesson_reviews_delete_own
  ON public.lesson_reviews
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
