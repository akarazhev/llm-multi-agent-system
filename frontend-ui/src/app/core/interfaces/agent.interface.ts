export interface Agent {
  agent_id: string;
  name: string;
  role: AgentRole;
  status: AgentStatus;
  description: string;
  capabilities: string[];
  current_task?: string;
  completed_tasks: number;
  failed_tasks: number;
  avg_task_duration?: number; // in minutes
  created_at: string;
  last_active?: string;
  configuration: AgentConfiguration;
  metrics: AgentMetrics;
  assigned_projects?: string[]; // project IDs
}

export interface AgentConfiguration {
  model: string; // e.g., "llama3-70b", "gpt-4"
  temperature: number;
  max_tokens: number;
  system_prompt?: string;
  tools_enabled: string[];
  auto_approve: boolean;
  max_retries: number;
}

export interface AgentMetrics {
  total_tasks: number;
  success_rate: number; // percentage
  avg_response_time: number; // in seconds
  tokens_used: number;
  cost_estimate: number; // in USD
}

export interface AgentTemplate {
  template_id: string;
  name: string;
  role: AgentRole;
  description: string;
  icon: string;
  capabilities: string[];
  default_configuration: AgentConfiguration;
  recommended_for: string[];
}

export enum AgentRole {
  BUSINESS_ANALYST = 'business_analyst',
  DEVELOPER = 'developer',
  QA_ENGINEER = 'qa_engineer',
  DEVOPS_ENGINEER = 'devops_engineer',
  TECHNICAL_WRITER = 'technical_writer',
  ARCHITECT = 'architect',
  PRODUCT_MANAGER = 'product_manager',
  SECURITY_ENGINEER = 'security_engineer'
}

export enum AgentStatus {
  IDLE = 'idle',
  WORKING = 'working',
  WAITING = 'waiting',
  COMPLETED = 'completed',
  ERROR = 'error',
  OFFLINE = 'offline'
}

export interface AgentTask {
  task_id: string;
  description: string;
  agent_role: AgentRole;
  status: string;
  created_at: string;
  completed_at?: string;
  error?: string;
}

export interface CreateAgentRequest {
  name: string;
  role: AgentRole;
  description?: string;
  configuration?: Partial<AgentConfiguration>;
  template_id?: string;
}
