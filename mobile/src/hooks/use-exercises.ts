import { useQuery } from '@tanstack/react-query';
import { exercisesApi } from '../lib/api-client';

export const exerciseKeys = {
  all: ['exercises'] as const,
  list: () => [...exerciseKeys.all, 'list'] as const,
  detail: (id: string) => [...exerciseKeys.all, 'detail', id] as const,
};

export function useExerciseCatalog() {
  return useQuery({
    queryKey: exerciseKeys.list(),
    queryFn: () => exercisesApi.listExercises(),
  });
}

export function useExercise(exerciseId: string) {
  return useQuery({
    queryKey: exerciseKeys.detail(exerciseId),
    queryFn: () => exercisesApi.getExercise(exerciseId),
    enabled: Boolean(exerciseId),
  });
}
