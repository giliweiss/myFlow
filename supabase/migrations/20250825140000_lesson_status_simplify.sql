-- Simplify lesson statuses to upcoming, completed, cancelled

ALTER TABLE public.lessons
  DROP CONSTRAINT lessons_status_check;

UPDATE public.lessons
SET status = 'upcoming'
WHERE status IN ('draft', 'planned');

UPDATE public.lessons
SET status = 'completed'
WHERE status = 'taught';

ALTER TABLE public.lessons
  ADD CONSTRAINT lessons_status_check CHECK (
    status IN ('upcoming', 'completed', 'cancelled')
  );

ALTER TABLE public.lessons
  ALTER COLUMN status SET DEFAULT 'upcoming';
