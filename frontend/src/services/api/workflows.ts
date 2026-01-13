/**
 * Workflows API Service
 * API calls for workflow management
 */

import { apiGet, apiPost, apiDelete } from './client';
import type { WorkflowRequest, WorkflowResponse, Workflow } from '../../types/workflow';

/**
 * Start a new workflow
 */
export async function startWorkflow(
  request: WorkflowRequest
): Promise<WorkflowResponse> {
  return apiPost<WorkflowResponse>('/api/workflows/start', request);
}

/**
 * Get workflow status
 */
export async function getWorkflowStatus(
  workflowId: string
): Promise<WorkflowResponse> {
  return apiGet<WorkflowResponse>(`/api/workflows/${workflowId}/status`);
}

/**
 * List all active workflows
 */
export async function listWorkflows(): Promise<Workflow[]> {
  return apiGet<Workflow[]>('/api/workflows');
}

/**
 * Cancel a workflow
 */
export async function cancelWorkflow(
  workflowId: string
): Promise<{ message: string }> {
  return apiDelete<{ message: string }>(`/api/workflows/${workflowId}/cancel`);
}
