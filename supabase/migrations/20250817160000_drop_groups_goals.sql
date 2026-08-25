-- Goals belong to lessons only; remove group-level goals.

ALTER TABLE public.groups
  DROP COLUMN goals;
