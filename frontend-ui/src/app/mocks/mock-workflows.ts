import {
  Workflow,
  WorkflowType,
  WorkflowStatus,
  WorkflowPriority,
  WorkflowTemplate,
  StepStatus
} from '../core/interfaces/workflow.interface';

/**
 * Workflow Templates - Pre-configured workflow templates
 */
export const WORKFLOW_TEMPLATES: WorkflowTemplate[] = [
  {
    template_id: 'tpl_feature_dev',
    name: 'Feature Development',
    description: 'End-to-end feature development from requirements to deployment',
    icon: '🚀',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    default_steps: [
      'Requirements Analysis',
      'Architecture Design',
      'Implementation',
      'Unit Testing',
      'Integration Testing',
      'Code Review',
      'Documentation',
      'Deployment'
    ],
    recommended_agents: ['agent_ba_001', 'agent_dev_001', 'agent_qa_001', 'agent_devops_001', 'agent_writer_001'],
    estimated_duration: 7200, // 2 hours
    tags: ['development', 'feature', 'full-cycle']
  },
  {
    template_id: 'tpl_bug_fix',
    name: 'Bug Fix',
    description: 'Investigate, fix, and test a bug',
    icon: '🐛',
    workflow_type: WorkflowType.BUG_FIX,
    default_steps: [
      'Bug Analysis',
      'Root Cause Investigation',
      'Fix Implementation',
      'Testing',
      'Regression Testing',
      'Documentation Update'
    ],
    recommended_agents: ['agent_dev_001', 'agent_qa_001'],
    estimated_duration: 1800, // 30 minutes
    tags: ['bugfix', 'maintenance', 'quick']
  },
  {
    template_id: 'tpl_code_review',
    name: 'Code Review',
    description: 'Comprehensive code review with security and quality checks',
    icon: '👀',
    workflow_type: WorkflowType.CODE_REVIEW,
    default_steps: [
      'Code Analysis',
      'Security Scan',
      'Quality Check',
      'Best Practices Review',
      'Performance Analysis',
      'Report Generation'
    ],
    recommended_agents: ['agent_dev_001', 'agent_arch_001'],
    estimated_duration: 900, // 15 minutes
    tags: ['review', 'quality', 'security']
  },
  {
    template_id: 'tpl_documentation',
    name: 'Documentation',
    description: 'Generate comprehensive project documentation',
    icon: '📝',
    workflow_type: WorkflowType.DOCUMENTATION,
    default_steps: [
      'Code Analysis',
      'API Documentation',
      'README Generation',
      'User Guide',
      'Architecture Diagram',
      'Deployment Guide'
    ],
    recommended_agents: ['agent_writer_001', 'agent_arch_001'],
    estimated_duration: 3600, // 1 hour
    tags: ['documentation', 'guides', 'reference']
  },
  {
    template_id: 'tpl_infrastructure',
    name: 'Infrastructure Setup',
    description: 'Set up CI/CD, monitoring, and deployment infrastructure',
    icon: '⚙️',
    workflow_type: WorkflowType.INFRASTRUCTURE,
    default_steps: [
      'Requirements Analysis',
      'CI/CD Pipeline Setup',
      'Monitoring Configuration',
      'Deployment Scripts',
      'Testing',
      'Documentation'
    ],
    recommended_agents: ['agent_devops_001'],
    estimated_duration: 5400, // 1.5 hours
    tags: ['infrastructure', 'devops', 'deployment']
  }
];

/**
 * Mock Workflows - Active and historical workflows
 */
export const MOCK_WORKFLOWS: Workflow[] = [
  {
    workflow_id: 'wf_20260114_001',
    name: 'User Authentication Feature',
    description: 'Implement JWT-based authentication system with refresh tokens',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    requirement: 'Add user authentication with JWT tokens, refresh token rotation, and secure session management',
    status: WorkflowStatus.RUNNING,
    started_at: '2026-01-14T10:30:00Z',
    duration: 3600,
    current_step: 'Implementation',
    completed_steps: ['Requirements Analysis', 'Architecture Design'],
    total_steps: 8,
    progress_percentage: 37.5,
    files_created: ['auth.service.ts', 'jwt.interceptor.ts', 'auth.guard.ts'],
    errors: [],
    project_id: 'proj-1',
    assigned_agents: ['agent_ba_001', 'agent_dev_001', 'agent_qa_001'],
    created_by: 'user_001',
    tags: ['authentication', 'security', 'backend'],
    priority: WorkflowPriority.HIGH,
    metrics: {
      total_duration: 3600,
      agent_time: {
        'agent_ba_001': 900,
        'agent_dev_001': 2700
      },
      files_generated: 3,
      lines_of_code: 450,
      tests_created: 0,
      cost_estimate: 1.25,
      success_rate: 100
    },
    steps: [
      {
        step_id: 'step_001',
        name: 'Requirements Analysis',
        description: 'Analyze authentication requirements and security constraints',
        status: StepStatus.COMPLETED,
        agent_id: 'agent_ba_001',
        started_at: '2026-01-14T10:30:00Z',
        completed_at: '2026-01-14T10:45:00Z',
        duration: 900,
        output: 'Requirements documented: JWT with 15min access tokens, 7-day refresh tokens, secure httpOnly cookies',
        logs: [
          'Started requirements analysis',
          'Identified security requirements',
          'Defined token lifecycle',
          'Completed analysis'
        ],
        artifacts: ['requirements.md']
      },
      {
        step_id: 'step_002',
        name: 'Architecture Design',
        description: 'Design authentication architecture and data flow',
        status: StepStatus.COMPLETED,
        agent_id: 'agent_arch_001',
        started_at: '2026-01-14T10:45:00Z',
        completed_at: '2026-01-14T11:00:00Z',
        duration: 900,
        output: 'Architecture designed with interceptor-based token refresh and secure storage',
        logs: [
          'Started architecture design',
          'Created system diagram',
          'Defined data flow',
          'Completed design'
        ],
        artifacts: ['architecture.md', 'flow-diagram.png']
      },
      {
        step_id: 'step_003',
        name: 'Implementation',
        description: 'Implement authentication services and guards',
        status: StepStatus.IN_PROGRESS,
        agent_id: 'agent_dev_001',
        started_at: '2026-01-14T11:00:00Z',
        logs: [
          'Started implementation',
          'Created AuthService',
          'Implementing JWT interceptor'
        ],
        artifacts: []
      }
    ],
    artifacts: [
      {
        artifact_id: 'art_001',
        type: 'documentation',
        name: 'Requirements Document',
        path: '/docs/authentication-requirements.md',
        size: 15420,
        created_at: '2026-01-14T10:45:00Z',
        created_by: 'agent_ba_001'
      },
      {
        artifact_id: 'art_002',
        type: 'diagram',
        name: 'Architecture Diagram',
        path: '/docs/auth-architecture.png',
        size: 125670,
        created_at: '2026-01-14T11:00:00Z',
        created_by: 'agent_arch_001'
      }
    ]
  },
  {
    workflow_id: 'wf_20260114_002',
    name: 'Payment Gateway Integration',
    description: 'Integrate Stripe payment processing',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    requirement: 'Integrate Stripe for payment processing with webhook handling',
    status: WorkflowStatus.COMPLETED,
    started_at: '2026-01-13T14:00:00Z',
    completed_at: '2026-01-13T18:30:00Z',
    duration: 16200,
    current_step: undefined,
    completed_steps: ['Analysis', 'Design', 'Implementation', 'Testing', 'Documentation', 'Deployment'],
    total_steps: 6,
    progress_percentage: 100,
    files_created: ['payment.service.ts', 'payment.controller.ts', 'webhook.handler.ts', 'payment.spec.ts'],
    errors: [],
    project_id: 'proj-1',
    assigned_agents: ['agent_ba_001', 'agent_dev_001', 'agent_qa_001', 'agent_devops_001'],
    created_by: 'user_001',
    tags: ['payment', 'integration', 'stripe'],
    priority: WorkflowPriority.CRITICAL,
    metrics: {
      total_duration: 16200,
      agent_time: {
        'agent_ba_001': 1800,
        'agent_dev_001': 10800,
        'agent_qa_001': 2700,
        'agent_devops_001': 900
      },
      files_generated: 4,
      lines_of_code: 850,
      tests_created: 12,
      cost_estimate: 4.5,
      success_rate: 100
    },
    steps: [],
    artifacts: []
  },
  {
    workflow_id: 'wf_20260114_003',
    name: 'Database Migration Bug',
    description: 'Fix failing database migration script',
    workflow_type: WorkflowType.BUG_FIX,
    requirement: 'Migration script fails on production database due to constraint conflict',
    status: WorkflowStatus.FAILED,
    started_at: '2026-01-14T09:00:00Z',
    completed_at: '2026-01-14T09:45:00Z',
    duration: 2700,
    current_step: undefined,
    completed_steps: ['Analysis', 'Fix Attempt'],
    total_steps: 4,
    progress_percentage: 50,
    files_created: [],
    errors: [
      {
        step: 'Fix Implementation',
        error: 'FOREIGN_KEY_CONSTRAINT_VIOLATION',
        message: 'Cannot drop column referenced by foreign key',
        stack_trace: 'at migration.ts:45\nat postgres.execute()',
        timestamp: '2026-01-14T09:40:00Z',
        severity: 'critical'
      }
    ],
    project_id: 'proj-2',
    assigned_agents: ['agent_dev_001'],
    created_by: 'user_002',
    tags: ['bugfix', 'database', 'migration'],
    priority: WorkflowPriority.CRITICAL,
    metrics: {
      total_duration: 2700,
      agent_time: {
        'agent_dev_001': 2700
      },
      files_generated: 0,
      lines_of_code: 0,
      tests_created: 0,
      cost_estimate: 0.75,
      success_rate: 0
    },
    steps: [],
    artifacts: []
  },
  {
    workflow_id: 'wf_20260113_001',
    name: 'API Documentation Update',
    description: 'Update API documentation for v2.0',
    workflow_type: WorkflowType.DOCUMENTATION,
    requirement: 'Generate comprehensive API documentation for new v2.0 endpoints',
    status: WorkflowStatus.COMPLETED,
    started_at: '2026-01-13T10:00:00Z',
    completed_at: '2026-01-13T12:00:00Z',
    duration: 7200,
    completed_steps: ['Analysis', 'Generation', 'Review', 'Publishing'],
    total_steps: 4,
    progress_percentage: 100,
    files_created: ['api-reference.md', 'openapi.yaml', 'postman-collection.json'],
    errors: [],
    project_id: 'proj-1',
    assigned_agents: ['agent_writer_001'],
    created_by: 'user_001',
    tags: ['documentation', 'api', 'v2'],
    priority: WorkflowPriority.MEDIUM,
    metrics: {
      total_duration: 7200,
      agent_time: {
        'agent_writer_001': 7200
      },
      files_generated: 3,
      lines_of_code: 0,
      tests_created: 0,
      cost_estimate: 2.0,
      success_rate: 100
    },
    steps: [],
    artifacts: []
  },
  {
    workflow_id: 'wf_20260114_004',
    name: 'Security Audit',
    description: 'Comprehensive security audit of authentication module',
    workflow_type: WorkflowType.CODE_REVIEW,
    requirement: 'Perform security audit on authentication and authorization code',
    status: WorkflowStatus.PENDING,
    started_at: '2026-01-14T15:00:00Z',
    completed_steps: [],
    total_steps: 6,
    progress_percentage: 0,
    files_created: [],
    errors: [],
    project_id: 'proj-1',
    assigned_agents: [],
    created_by: 'user_001',
    tags: ['security', 'audit', 'review'],
    priority: WorkflowPriority.HIGH,
    metrics: {
      total_duration: 0,
      agent_time: {},
      files_generated: 0,
      lines_of_code: 0,
      tests_created: 0,
      cost_estimate: 0,
      success_rate: 0
    },
    steps: [],
    artifacts: []
  }
];
