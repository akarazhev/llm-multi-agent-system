export interface Workflow {
  workflow_id: string;
  workflow_type: WorkflowType;
  requirement: string;
  status: WorkflowStatus;
  started_at: string;
  completed_at?: string;
  current_step?: string;
  completed_steps: string[];
  files_created: string[];
  errors: WorkflowError[];
}

export enum WorkflowType {
  FEATURE_DEVELOPMENT = 'feature_development',
  BUG_FIX = 'bug_fix',
  INFRASTRUCTURE = 'infrastructure',
  DOCUMENTATION = 'documentation',
  ANALYSIS = 'analysis'
}

export enum WorkflowStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export interface WorkflowError {
  step: string;
  error: string;
  timestamp: string;
}

export interface WorkflowCreateRequest {
  requirement: string;
  workflow_type: WorkflowType;
  context?: Record<string, any>;
}

export interface WorkflowState {
  workflow_id: string;
  requirement: string;
  workflow_type: string;
  status: string;
  current_step: string;
  completed_steps: string[];
  business_analysis?: any[];
  architecture?: any[];
  implementation?: any[];
  tests?: any[];
  infrastructure?: any[];
  documentation?: any[];
  files_created: string[];
  errors: WorkflowError[];
  started_at: string;
  completed_at?: string;
}
