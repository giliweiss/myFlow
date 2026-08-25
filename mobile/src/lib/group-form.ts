import type { Group, GroupLevel, UpdateGroupInput } from '../types/group';

const LEVEL_TO_DISPLAY: Record<GroupLevel, string> = {
  beginner: 'מתחיל',
  intermediate: 'בינוני',
  advanced: 'מתקדם',
};

const LEVEL_TO_API: Record<string, GroupLevel> = {
  מתחיל: 'beginner',
  בינוני: 'intermediate',
  מתקדם: 'advanced',
  beginner: 'beginner',
  intermediate: 'intermediate',
  advanced: 'advanced',
};

export interface GroupFormValues {
  name: string;
  level: string;
  duration: string;
  equipment: string;
  limitations: string;
  notes: string;
}

export function levelToDisplay(level: GroupLevel): string {
  return LEVEL_TO_DISPLAY[level];
}

export function levelToApi(levelText: string): GroupLevel {
  const normalized = levelText.trim();
  return LEVEL_TO_API[normalized] ?? 'intermediate';
}

export function parseCommaList(value: string): string[] {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

export function formatCommaList(items: string[]): string {
  return items.join(', ');
}

export function groupToFormValues(group: Group): GroupFormValues {
  return {
    name: group.name,
    level: levelToDisplay(group.level),
    duration: String(group.typical_duration_minutes),
    equipment: formatCommaList(group.available_equipment),
    limitations: formatCommaList(group.group_considerations),
    notes: group.notes ?? '',
  };
}

export function formValuesToUpdatePayload(values: GroupFormValues): UpdateGroupInput {
  const duration = Number.parseInt(values.duration, 10);

  return {
    name: values.name.trim(),
    level: levelToApi(values.level),
    typical_duration_minutes: Number.isFinite(duration) ? duration : undefined,
    available_equipment: parseCommaList(values.equipment),
    group_considerations: parseCommaList(values.limitations),
    notes: values.notes.trim() || null,
  };
}
