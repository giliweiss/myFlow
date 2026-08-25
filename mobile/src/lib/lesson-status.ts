import type { BadgeVariant } from '../components/ui/Badge';
import type { LessonStatus } from '../types/lesson';
import { strings } from '../i18n/he';

export const STATUS_LABELS: Record<LessonStatus, string> = {
  draft: strings.lessons.draft,
  planned: strings.lessons.planned,
  taught: strings.lessons.taught,
  cancelled: strings.lessons.cancelled,
};

export const STATUS_VARIANTS: Record<LessonStatus, BadgeVariant> = {
  draft: 'status-draft',
  planned: 'status-planned',
  taught: 'status-taught',
  cancelled: 'status-cancelled',
};

export function getSelectableStatuses(currentStatus: LessonStatus): LessonStatus[] {
  switch (currentStatus) {
    case 'draft':
      return ['draft', 'planned', 'cancelled'];
    case 'planned':
      return ['planned', 'taught', 'cancelled'];
    case 'taught':
      return ['taught'];
    case 'cancelled':
      return ['cancelled'];
    default:
      return [currentStatus];
  }
}

export function isLessonEditable(status: LessonStatus): boolean {
  return status === 'draft' || status === 'planned';
}
