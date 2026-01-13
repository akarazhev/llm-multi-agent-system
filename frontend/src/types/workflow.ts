/**
 * Workflow Types
 * Based on FastAPI backend API models
 */

export type WorkflowStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface WorkflowRequest {
  requirements: string;
  request_id?: string;
}

export interface WorkflowResponse {
  request_id: string;
  workflow_id: string;
  status: WorkflowStatus;
  current_step?: string;
  message?: string;
}

export interface Workflow {
  workflow_id: string;
  request_id: string;
  status: WorkflowStatus;
  current_step?: number;
  total_steps?: number;
  current_agent?: string;
  message?: string;
  error?: string;
  created_at?: string;
  updated_at?: string;
  completed_at?: string;
}
