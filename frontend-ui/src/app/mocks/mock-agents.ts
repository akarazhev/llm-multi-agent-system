import { Agent, AgentRole, AgentStatus, AgentTemplate } from '../core/interfaces/agent.interface';

/**
 * Agent Templates - Pre-configured agent templates for quick setup
 */
export const AGENT_TEMPLATES: AgentTemplate[] = [
  {
    template_id: 'tpl_business_analyst',
    name: 'Business Analyst',
    role: AgentRole.BUSINESS_ANALYST,
    description: 'Analyzes requirements, creates user stories, and defines acceptance criteria',
    icon: '📊',
    capabilities: [
      'Requirements Analysis',
      'User Story Creation',
      'Acceptance Criteria Definition',
      'Stakeholder Communication',
      'Documentation'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.7,
      max_tokens: 4000,
      tools_enabled: ['document_analysis', 'requirements_extraction'],
      auto_approve: false,
      max_retries: 3
    },
    recommended_for: ['Product Development', 'Feature Planning', 'Requirements Gathering']
  },
  {
    template_id: 'tpl_developer',
    name: 'Full-Stack Developer',
    role: AgentRole.DEVELOPER,
    description: 'Writes code, implements features, and fixes bugs across the stack',
    icon: '👨‍💻',
    capabilities: [
      'Code Generation',
      'Bug Fixing',
      'Feature Implementation',
      'Code Refactoring',
      'API Development',
      'Database Design'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.3,
      max_tokens: 8000,
      tools_enabled: ['code_execution', 'file_operations', 'git_operations'],
      auto_approve: false,
      max_retries: 2
    },
    recommended_for: ['Feature Development', 'Bug Fixes', 'Code Refactoring']
  },
  {
    template_id: 'tpl_qa_engineer',
    name: 'QA Engineer',
    role: AgentRole.QA_ENGINEER,
    description: 'Creates test plans, writes automated tests, and ensures quality',
    icon: '🧪',
    capabilities: [
      'Test Case Creation',
      'Automated Testing',
      'Test Plan Development',
      'Bug Reporting',
      'Quality Assurance',
      'Performance Testing'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.4,
      max_tokens: 6000,
      tools_enabled: ['test_execution', 'bug_tracking'],
      auto_approve: false,
      max_retries: 3
    },
    recommended_for: ['Testing', 'Quality Assurance', 'Test Automation']
  },
  {
    template_id: 'tpl_devops_engineer',
    name: 'DevOps Engineer',
    role: AgentRole.DEVOPS_ENGINEER,
    description: 'Manages infrastructure, CI/CD pipelines, and deployment automation',
    icon: '⚙️',
    capabilities: [
      'CI/CD Pipeline Setup',
      'Infrastructure as Code',
      'Deployment Automation',
      'Monitoring Setup',
      'Container Orchestration',
      'Cloud Management'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.3,
      max_tokens: 6000,
      tools_enabled: ['deployment', 'infrastructure', 'monitoring'],
      auto_approve: false,
      max_retries: 2
    },
    recommended_for: ['Deployment', 'Infrastructure', 'CI/CD']
  },
  {
    template_id: 'tpl_technical_writer',
    name: 'Technical Writer',
    role: AgentRole.TECHNICAL_WRITER,
    description: 'Creates documentation, API references, and user guides',
    icon: '📝',
    capabilities: [
      'API Documentation',
      'User Guide Creation',
      'README Generation',
      'Code Comments',
      'Tutorial Writing',
      'Release Notes'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.6,
      max_tokens: 8000,
      tools_enabled: ['document_generation', 'markdown_formatting'],
      auto_approve: false,
      max_retries: 2
    },
    recommended_for: ['Documentation', 'Knowledge Base', 'User Guides']
  },
  {
    template_id: 'tpl_architect',
    name: 'Software Architect',
    role: AgentRole.ARCHITECT,
    description: 'Designs system architecture, makes technical decisions, and ensures scalability',
    icon: '🏗️',
    capabilities: [
      'Architecture Design',
      'Technical Decision Making',
      'System Design',
      'Technology Selection',
      'Scalability Planning',
      'Security Architecture'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.5,
      max_tokens: 6000,
      tools_enabled: ['diagram_generation', 'architecture_analysis'],
      auto_approve: false,
      max_retries: 2
    },
    recommended_for: ['System Design', 'Architecture Planning', 'Technical Strategy']
  },
  {
    template_id: 'tpl_security_engineer',
    name: 'Security Engineer',
    role: AgentRole.SECURITY_ENGINEER,
    description: 'Performs security audits, identifies vulnerabilities, and implements security measures',
    icon: '🔒',
    capabilities: [
      'Security Audits',
      'Vulnerability Assessment',
      'Penetration Testing',
      'Security Best Practices',
      'Code Security Review',
      'Compliance Checking'
    ],
    default_configuration: {
      model: 'llama3-70b',
      temperature: 0.2,
      max_tokens: 6000,
      tools_enabled: ['security_scan', 'vulnerability_check'],
      auto_approve: false,
      max_retries: 3
    },
    recommended_for: ['Security Audit', 'Vulnerability Assessment', 'Compliance']
  }
];

/**
 * Mock Agents - Active agents in the system
 */
export const MOCK_AGENTS: Agent[] = [
  {
    agent_id: 'agent_ba_001',
    name: 'Alice - BA',
    role: AgentRole.BUSINESS_ANALYST,
    status: AgentStatus.IDLE,
    description: 'Senior business analyst specializing in fintech requirements',
    capabilities: ['Requirements Analysis', 'User Story Creation', 'Stakeholder Communication'],
    completed_tasks: 45,
    failed_tasks: 2,
    avg_task_duration: 25,
    created_at: '2026-01-01T10:00:00Z',
    last_active: '2026-01-14T14:30:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.7,
      max_tokens: 4000,
      tools_enabled: ['document_analysis', 'requirements_extraction'],
      auto_approve: false,
      max_retries: 3
    },
    metrics: {
      total_tasks: 47,
      success_rate: 95.7,
      avg_response_time: 12.5,
      tokens_used: 1250000,
      cost_estimate: 2.5
    },
    assigned_projects: ['proj-1']
  },
  {
    agent_id: 'agent_dev_001',
    name: 'Bob - Developer',
    role: AgentRole.DEVELOPER,
    status: AgentStatus.WORKING,
    description: 'Full-stack developer with expertise in Angular and Python',
    capabilities: ['Code Generation', 'Bug Fixing', 'API Development'],
    completed_tasks: 128,
    failed_tasks: 8,
    avg_task_duration: 45,
    current_task: 'Implementing user authentication module',
    created_at: '2026-01-01T10:00:00Z',
    last_active: '2026-01-14T15:45:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.3,
      max_tokens: 8000,
      tools_enabled: ['code_execution', 'file_operations', 'git_operations'],
      auto_approve: false,
      max_retries: 2
    },
    metrics: {
      total_tasks: 136,
      success_rate: 94.1,
      avg_response_time: 18.2,
      tokens_used: 3200000,
      cost_estimate: 6.4
    },
    assigned_projects: ['proj-1', 'proj-2']
  },
  {
    agent_id: 'agent_qa_001',
    name: 'Charlie - QA',
    role: AgentRole.QA_ENGINEER,
    status: AgentStatus.IDLE,
    description: 'QA engineer focused on test automation and quality assurance',
    capabilities: ['Test Case Creation', 'Automated Testing', 'Bug Reporting'],
    completed_tasks: 92,
    failed_tasks: 5,
    avg_task_duration: 30,
    created_at: '2026-01-01T10:00:00Z',
    last_active: '2026-01-14T13:20:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.4,
      max_tokens: 6000,
      tools_enabled: ['test_execution', 'bug_tracking'],
      auto_approve: false,
      max_retries: 3
    },
    metrics: {
      total_tasks: 97,
      success_rate: 94.8,
      avg_response_time: 15.1,
      tokens_used: 1800000,
      cost_estimate: 3.6
    },
    assigned_projects: ['proj-1']
  },
  {
    agent_id: 'agent_devops_001',
    name: 'David - DevOps',
    role: AgentRole.DEVOPS_ENGINEER,
    status: AgentStatus.WORKING,
    description: 'DevOps engineer specializing in Kubernetes and AWS',
    capabilities: ['CI/CD Pipeline Setup', 'Infrastructure as Code', 'Deployment Automation'],
    completed_tasks: 76,
    failed_tasks: 4,
    avg_task_duration: 35,
    current_task: 'Setting up production deployment pipeline',
    created_at: '2026-01-01T10:00:00Z',
    last_active: '2026-01-14T15:50:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.3,
      max_tokens: 6000,
      tools_enabled: ['deployment', 'infrastructure', 'monitoring'],
      auto_approve: false,
      max_retries: 2
    },
    metrics: {
      total_tasks: 80,
      success_rate: 95.0,
      avg_response_time: 16.8,
      tokens_used: 1950000,
      cost_estimate: 3.9
    },
    assigned_projects: ['proj-2', 'proj-3']
  },
  {
    agent_id: 'agent_writer_001',
    name: 'Emma - Writer',
    role: AgentRole.TECHNICAL_WRITER,
    status: AgentStatus.IDLE,
    description: 'Technical writer creating comprehensive documentation',
    capabilities: ['API Documentation', 'User Guide Creation', 'Tutorial Writing'],
    completed_tasks: 54,
    failed_tasks: 1,
    avg_task_duration: 40,
    created_at: '2026-01-01T10:00:00Z',
    last_active: '2026-01-14T12:10:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.6,
      max_tokens: 8000,
      tools_enabled: ['document_generation', 'markdown_formatting'],
      auto_approve: false,
      max_retries: 2
    },
    metrics: {
      total_tasks: 55,
      success_rate: 98.2,
      avg_response_time: 14.3,
      tokens_used: 1650000,
      cost_estimate: 3.3
    },
    assigned_projects: ['proj-1', 'proj-2']
  },
  {
    agent_id: 'agent_arch_001',
    name: 'Frank - Architect',
    role: AgentRole.ARCHITECT,
    status: AgentStatus.IDLE,
    description: 'Software architect designing scalable systems',
    capabilities: ['Architecture Design', 'Technical Decision Making', 'System Design'],
    completed_tasks: 32,
    failed_tasks: 1,
    avg_task_duration: 60,
    created_at: '2026-01-05T10:00:00Z',
    last_active: '2026-01-14T11:00:00Z',
    configuration: {
      model: 'llama3-70b',
      temperature: 0.5,
      max_tokens: 6000,
      tools_enabled: ['diagram_generation', 'architecture_analysis'],
      auto_approve: false,
      max_retries: 2
    },
    metrics: {
      total_tasks: 33,
      success_rate: 97.0,
      avg_response_time: 20.5,
      tokens_used: 1100000,
      cost_estimate: 2.2
    },
    assigned_projects: ['proj-3']
  }
];
