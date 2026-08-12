-- Lesson attendance per group member

CREATE TABLE public.lesson_attendance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid NOT NULL REFERENCES public.lessons (id) ON DELETE CASCADE,
  group_member_id uuid NOT NULL REFERENCES public.group_members (id) ON DELETE CASCADE,
  registered boolean NOT NULL DEFAULT false,
  attended boolean NOT NULL DEFAULT false,

  CONSTRAINT lesson_attendance_unique_member UNIQUE (lesson_id, group_member_id)
);

CREATE INDEX lesson_attendance_lesson_id_idx ON public.lesson_attendance (lesson_id);
CREATE INDEX lesson_attendance_group_member_id_idx ON public.lesson_attendance (group_member_id);

ALTER TABLE public.lesson_attendance ENABLE ROW LEVEL SECURITY;

CREATE POLICY lesson_attendance_select_own
  ON public.lesson_attendance
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

CREATE POLICY lesson_attendance_insert_own
  ON public.lesson_attendance
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

CREATE POLICY lesson_attendance_update_own
  ON public.lesson_attendance
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

CREATE POLICY lesson_attendance_delete_own
  ON public.lesson_attendance
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
