export interface Agent {
  agent_id: string;
  role: AgentRole;
  status: AgentStatus;
  current_task?: string;
  completed_tasks: number;
}

export enum AgentRole {
  BUSINESS_ANALYST = 'business_analyst',
  DEVELOPER = 'developer',
  QA_ENGINEER = 'qa_engineer',
  DEVOPS_ENGINEER = 'devops_engineer',
  TECHNICAL_WRITER = 'technical_writer'
}

export enum AgentStatus {
  IDLE = 'idle',
  WORKING = 'working',
  WAITING = 'waiting',
  COMPLETED = 'completed',
  ERROR = 'error'
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
