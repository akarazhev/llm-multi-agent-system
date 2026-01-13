export type ProjectStatus = 'active' | 'planning' | 'on_hold' | 'archived' | 'completed';
export type ProjectType = 'web_app' | 'mobile_app' | 'api' | 'infrastructure' | 'data' | 'custom';
export type AccessLevel = 'owner' | 'admin' | 'developer' | 'viewer';

export interface Project {
  id: string;
  name: string;
  description: string;
  icon?: string;
  status: ProjectStatus;
  type: ProjectType;
  
  // Team
  ownerId: string;
  teamMembers: TeamMember[];
  aiAgents: string[]; // Agent IDs
  
  // Integrations
  integrations: ProjectIntegrations;
  
  // Technology Stack
  techStack: TechStack;
  
  // Statistics
  stats: ProjectStats;
  
  // Metadata
  createdAt: string;
  updatedAt: string;
  lastActivity?: string;
}

export interface TeamMember {
  userId: string;
  name: string;
  email: string;
  role: string;
  accessLevel: AccessLevel;
  avatar?: string;
  joinedAt: string;
}

export interface ProjectIntegrations {
  git?: GitIntegration;
  jira?: JiraIntegration;
  confluence?: ConfluenceIntegration;
  slack?: SlackIntegration;
}

export interface GitIntegration {
  platform: 'github' | 'gitlab' | 'bitbucket';
  url: string;
  branch: string;
  connected: boolean;
  lastSync?: string;
}

export interface JiraIntegration {
  url: string;
  projectKey: string;
  connected: boolean;
  lastSync?: string;
}

export interface ConfluenceIntegration {
  spaceKey: string;
  connected: boolean;
  lastSync?: string;
}

export interface SlackIntegration {
  channel: string;
  connected: boolean;
}

export interface TechStack {
  languages: string[];
  frameworks: string[];
  databases: string[];
  tools: string[];
}

export interface ProjectStats {
  totalWorkflows: number;
  activeWorkflows: number;
  completedWorkflows: number;
  failedWorkflows: number;
  teamSize: number;
  aiAgentsCount: number;
  filesGenerated: number;
  linesOfCode: number;
}

export interface ProjectFormData {
  name: string;
  description: string;
  icon?: string;
  status: ProjectStatus;
  type: ProjectType;
  techStack: TechStack;
}
