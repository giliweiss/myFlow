import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { lessonsApi } from '../lib/api-client';
import type { CreateLessonInput, Lesson, UpdateLessonInput } from '../types/lesson';

export const lessonKeys = {
  all: ['lessons'] as const,
  groupList: (groupId: string) => [...lessonKeys.all, 'group', groupId] as const,
  detail: (lessonId: string) => [...lessonKeys.all, 'detail', lessonId] as const,
};

export function useGroupLessons(groupId: string | undefined) {
  return useQuery({
    queryKey: lessonKeys.groupList(groupId ?? ''),
    queryFn: () => lessonsApi.getGroupLessons(groupId!),
    enabled: Boolean(groupId),
  });
}

export function useLesson(lessonId: string | undefined) {
  return useQuery({
    queryKey: lessonKeys.detail(lessonId ?? ''),
    queryFn: () => lessonsApi.getLesson(lessonId!),
    enabled: Boolean(lessonId),
  });
}

export function useCreateLesson(groupId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreateLessonInput) => {
      if (!groupId) {
        throw new Error('Group id is required');
      }
      return lessonsApi.createLesson(groupId, input);
    },
    onSuccess: (lesson: Lesson) => {
      queryClient.invalidateQueries({ queryKey: lessonKeys.groupList(lesson.group_id) });
      queryClient.setQueryData(lessonKeys.detail(lesson.id), lesson);
    },
  });
}

export function useUpdateLesson(lessonId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (updates: UpdateLessonInput) => {
      if (!lessonId) {
        throw new Error('Lesson id is required');
      }
      return lessonsApi.updateLesson(lessonId, updates);
    },
    onSuccess: (lesson: Lesson) => {
      queryClient.setQueryData(lessonKeys.detail(lesson.id), lesson);
      queryClient.invalidateQueries({ queryKey: lessonKeys.groupList(lesson.group_id) });
    },
  });
}
