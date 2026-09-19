import type { BadgeVariant } from '../components/ui/Badge';
import type { LessonStatus } from '../types/lesson';
import { strings } from '../i18n/he';

export const STATUS_LABELS: Record<LessonStatus, string> = {
  upcoming: strings.lessons.upcoming,
  completed: strings.lessons.completed,
  cancelled: strings.lessons.cancelled,
};

export const STATUS_VARIANTS: Record<LessonStatus, BadgeVariant> = {
  upcoming: 'status-upcoming',
  completed: 'status-completed',
  cancelled: 'status-cancelled',
};

export function getSelectableStatuses(currentStatus: LessonStatus): LessonStatus[] {
  switch (currentStatus) {
    case 'upcoming':
      return ['upcoming', 'completed', 'cancelled'];
    case 'completed':
      return ['completed'];
    case 'cancelled':
      return ['cancelled'];
    default:
      return [currentStatus];
  }
}

export function isLessonEditable(status: LessonStatus): boolean {
  return status === 'upcoming';
}

export function normalizeLessonStatus(status: string): LessonStatus {
  switch (status) {
    case 'upcoming':
    case 'completed':
    case 'cancelled':
      return status;
    case 'draft':
    case 'planned':
      return 'upcoming';
    case 'taught':
      return 'completed';
    default:
      return 'upcoming';
  }
}
