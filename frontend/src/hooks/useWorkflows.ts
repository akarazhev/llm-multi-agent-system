/**
 * Workflows React Query Hooks
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { startWorkflow, getWorkflowStatus, listWorkflows, cancelWorkflow } from '@services/api/workflows';
import type { WorkflowRequest, WorkflowResponse, Workflow } from '@/types/workflow';

// Query keys
export const workflowKeys = {
  all: ['workflows'] as const,
  lists: () => [...workflowKeys.all, 'list'] as const,
  list: () => [...workflowKeys.lists()] as const,
  details: () => [...workflowKeys.all, 'detail'] as const,
  detail: (id: string) => [...workflowKeys.details(), id] as const,
};

/**
 * Hook to list all workflows
 */
export function useWorkflows() {
  return useQuery<Workflow[]>({
    queryKey: workflowKeys.list(),
    queryFn: listWorkflows,
    refetchInterval: 5000, // Poll every 5 seconds for real-time updates
  });
}

/**
 * Hook to get workflow status
 */
export function useWorkflowStatus(workflowId: string | null) {
  return useQuery<WorkflowResponse>({
    queryKey: workflowKeys.detail(workflowId || ''),
    queryFn: () => getWorkflowStatus(workflowId!),
    enabled: !!workflowId,
    refetchInterval: (query) => {
      const data = query.state.data as WorkflowResponse | undefined;
      if (data && (data.status === 'running' || data.status === 'pending')) {
        return 2000; // Poll every 2 seconds for active workflows
      }
      return false; // Don't poll for completed/failed/cancelled workflows
    },
  });
}

/**
 * Hook to start a new workflow
 */
export function useStartWorkflow() {
  const queryClient = useQueryClient();

  return useMutation<WorkflowResponse, Error, WorkflowRequest>({
    mutationFn: startWorkflow,
    onSuccess: () => {
      // Invalidate workflows list to refetch
      queryClient.invalidateQueries({ queryKey: workflowKeys.list() });
    },
  });
}

/**
 * Hook to cancel a workflow
 */
export function useCancelWorkflow() {
  const queryClient = useQueryClient();

  return useMutation<{ message: string }, Error, string>({
    mutationFn: cancelWorkflow,
    onSuccess: (_, workflowId) => {
      // Invalidate specific workflow and list
      queryClient.invalidateQueries({ queryKey: workflowKeys.detail(workflowId) });
      queryClient.invalidateQueries({ queryKey: workflowKeys.list() });
    },
  });
}
