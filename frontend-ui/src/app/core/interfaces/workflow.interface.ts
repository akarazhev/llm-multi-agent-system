export interface Workflow {
  workflow_id: string;
  name: string;
  description: string;
  workflow_type: WorkflowType;
  requirement: string;
  status: WorkflowStatus;
  started_at: string;
  completed_at?: string;
  duration?: number; // in seconds
  current_step?: string;
  completed_steps: string[];
  total_steps: number;
  progress_percentage: number;
  files_created: string[];
  errors: WorkflowError[];
  project_id?: string;
  assigned_agents: string[]; // agent IDs
  created_by: string; // user ID
  tags: string[];
  priority: WorkflowPriority;
  metrics: WorkflowMetrics;
  steps: WorkflowStep[];
  artifacts: WorkflowArtifact[];
}

export enum WorkflowType {
  FEATURE_DEVELOPMENT = 'feature_development',
  BUG_FIX = 'bug_fix',
  INFRASTRUCTURE = 'infrastructure',
  DOCUMENTATION = 'documentation',
  ANALYSIS = 'analysis',
  CODE_REVIEW = 'code_review',
  TESTING = 'testing',
  DEPLOYMENT = 'deployment',
  REFACTORING = 'refactoring'
}

export enum WorkflowStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum WorkflowPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum StepStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  SKIPPED = 'skipped'
}

export interface WorkflowError {
  step: string;
  error: string;
  message: string;
  stack_trace?: string;
  timestamp: string;
  severity: 'warning' | 'error' | 'critical';
}

export interface WorkflowStep {
  step_id: string;
  name: string;
  description: string;
  status: StepStatus;
  agent_id?: string;
  started_at?: string;
  completed_at?: string;
  duration?: number;
  output?: string;
  logs: string[];
  artifacts: string[];
}

export interface WorkflowMetrics {
  total_duration: number; // seconds
  agent_time: Record<string, number>; // agent_id -> seconds
  files_generated: number;
  lines_of_code: number;
  tests_created: number;
  cost_estimate: number;
  success_rate: number;
}

export interface WorkflowArtifact {
  artifact_id: string;
  type: 'code' | 'documentation' | 'test' | 'config' | 'diagram';
  name: string;
  path: string;
  size: number;
  created_at: string;
  created_by: string; // agent_id
}

export interface WorkflowCreateRequest {
  name: string;
  description?: string;
  requirement: string;
  workflow_type: WorkflowType;
  project_id?: string;
  assigned_agents?: string[];
  priority?: WorkflowPriority;
  tags?: string[];
  context?: Record<string, any>;
}

export interface WorkflowTemplate {
  template_id: string;
  name: string;
  description: string;
  icon: string;
  workflow_type: WorkflowType;
  default_steps: string[];
  recommended_agents: string[];
  estimated_duration: number;
  tags: string[];
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
