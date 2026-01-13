/**
 * Agents API Service
 * API calls for agent information
 */

import { apiGet } from './client';
import type { AgentInfo } from '../../types/agent';

/**
 * Get all registered agents
 */
export async function getAgents(): Promise<AgentInfo[]> {
  return apiGet<AgentInfo[]>('/api/agents');
}

/**
 * Get agent by ID
 */
export async function getAgent(agentId: string): Promise<AgentInfo> {
  return apiGet<AgentInfo>(`/api/agents/${agentId}`);
}
