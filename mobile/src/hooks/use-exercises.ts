import { useQuery } from '@tanstack/react-query';
import { exercisesApi } from '../lib/api-client';

export const exerciseKeys = {
  all: ['exercises'] as const,
  list: () => [...exerciseKeys.all, 'list'] as const,
};

export function useExerciseCatalog() {
  return useQuery({
    queryKey: exerciseKeys.list(),
    queryFn: () => exercisesApi.listExercises(),
  });
}
