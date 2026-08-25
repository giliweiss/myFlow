import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { groupsApi } from '../lib/api-client';
import type { Group, UpdateGroupInput } from '../types/group';

export const groupKeys = {
  all: ['groups'] as const,
  list: () => [...groupKeys.all, 'list'] as const,
  detail: (groupId: string) => [...groupKeys.all, 'detail', groupId] as const,
};

export function useGroups() {
  return useQuery({
    queryKey: groupKeys.list(),
    queryFn: () => groupsApi.getGroups(),
  });
}

export function useGroup(groupId: string | undefined) {
  return useQuery({
    queryKey: groupKeys.detail(groupId ?? ''),
    queryFn: () => groupsApi.getGroup(groupId!),
    enabled: Boolean(groupId),
  });
}

export function useUpdateGroup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      groupId,
      updates,
    }: {
      groupId: string;
      updates: UpdateGroupInput;
    }) => groupsApi.updateGroup(groupId, updates),
    onSuccess: (updatedGroup: Group) => {
      queryClient.setQueryData(groupKeys.detail(updatedGroup.id), updatedGroup);
      queryClient.invalidateQueries({ queryKey: groupKeys.list() });
    },
  });
}
