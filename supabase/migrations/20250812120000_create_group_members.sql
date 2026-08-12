-- Group roster (lightweight members without accounts)

CREATE TABLE public.group_members (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  group_id uuid NOT NULL REFERENCES public.groups (id) ON DELETE CASCADE,
  name text NOT NULL,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);

CREATE INDEX group_members_group_id_idx ON public.group_members (group_id);
CREATE INDEX group_members_is_active_idx ON public.group_members (is_active);

CREATE TRIGGER group_members_set_updated_at
  BEFORE UPDATE ON public.group_members
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();

ALTER TABLE public.group_members ENABLE ROW LEVEL SECURITY;

CREATE POLICY group_members_select_own
  ON public.group_members
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

CREATE POLICY group_members_insert_own
  ON public.group_members
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

CREATE POLICY group_members_update_own
  ON public.group_members
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

CREATE POLICY group_members_delete_own
  ON public.group_members
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
