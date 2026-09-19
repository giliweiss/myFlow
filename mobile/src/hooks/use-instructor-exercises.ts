import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { instructorExercisesApi } from '../lib/api-client';
import type {
  CreateInstructorExerciseInput,
  UpdateInstructorExerciseInput,
} from '../types/instructor-exercise';

export const instructorExerciseKeys = {
  all: ['instructor-exercises'] as const,
  list: () => [...instructorExerciseKeys.all, 'list'] as const,
  detail: (id: string) => [...instructorExerciseKeys.all, 'detail', id] as const,
};

export function useInstructorExercises() {
  return useQuery({
    queryKey: instructorExerciseKeys.list(),
    queryFn: () => instructorExercisesApi.listExercises(),
  });
}

export function useInstructorExercise(exerciseId: string) {
  return useQuery({
    queryKey: instructorExerciseKeys.detail(exerciseId),
    queryFn: () => instructorExercisesApi.getExercise(exerciseId),
    enabled: Boolean(exerciseId),
  });
}

export function useCreateInstructorExercise() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreateInstructorExerciseInput) =>
      instructorExercisesApi.createExercise(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instructorExerciseKeys.all });
    },
  });
}

export function useUpdateInstructorExercise(exerciseId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: UpdateInstructorExerciseInput) =>
      instructorExercisesApi.updateExercise(exerciseId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instructorExerciseKeys.all });
    },
  });
}

export function useArchiveInstructorExercise() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (exerciseId: string) =>
      instructorExercisesApi.archiveExercise(exerciseId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instructorExerciseKeys.all });
    },
  });
}
