/**
 * Agent Types
 * Based on FastAPI backend API models
 */

export interface AgentTool {
  name: string;
  description?: string;
  parameters?: Record<string, unknown>;
}

export interface AgentInfo {
  agent_id: string;
  agent_name: string;
  name?: string;
  tools: (AgentTool | string)[];
  status?: 'active' | 'idle' | 'error' | 'available' | 'offline';
  current_task?: string;
  execution_time?: string;
}
