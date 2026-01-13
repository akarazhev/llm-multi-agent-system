/**
 * Agents React Query Hooks
 */

import { useQuery } from '@tanstack/react-query';
import { getAgents, getAgent } from '@services/api/agents';
import type { AgentInfo } from '@/types/agent';

// Query keys
export const agentKeys = {
  all: ['agents'] as const,
  lists: () => [...agentKeys.all, 'list'] as const,
  list: () => [...agentKeys.lists()] as const,
  details: () => [...agentKeys.all, 'detail'] as const,
  detail: (id: string) => [...agentKeys.details(), id] as const,
};

/**
 * Hook to get all agents
 */
export function useAgents() {
  return useQuery<AgentInfo[]>({
    queryKey: agentKeys.list(),
    queryFn: getAgents,
    refetchInterval: 10000, // Poll every 10 seconds for agent status updates
  });
}

/**
 * Hook to get a specific agent
 */
export function useAgent(agentId: string | null) {
  return useQuery<AgentInfo>({
    queryKey: agentKeys.detail(agentId || ''),
    queryFn: () => getAgent(agentId!),
    enabled: !!agentId,
  });
}
