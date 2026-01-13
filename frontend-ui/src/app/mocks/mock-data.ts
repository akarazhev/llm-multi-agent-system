import { Workflow, WorkflowStatus, WorkflowType, WorkflowState } from '../core/interfaces/workflow.interface';

// Export agents from the new centralized file
export { MOCK_AGENTS, AGENT_TEMPLATES } from './mock-agents';

/**
 * Mock Workflows Data
 */
export const MOCK_WORKFLOWS: Workflow[] = [
  {
    workflow_id: 'workflow_20260114_103022',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    requirement: 'Create a REST API for user authentication with JWT tokens, OAuth2 integration, and role-based access control',
    status: WorkflowStatus.RUNNING,
    started_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 min ago
    current_step: 'implementation',
    completed_steps: ['business_analyst', 'architecture_design'],
    files_created: [
      'src/auth/auth.controller.ts',
      'src/auth/auth.service.ts',
      'src/auth/jwt.strategy.ts',
      'src/auth/auth.module.ts'
    ],
    errors: []
  },
  {
    workflow_id: 'workflow_20260114_093510',
    workflow_type: WorkflowType.BUG_FIX,
    requirement: 'Fix memory leak in WebSocket connection handler causing server crashes after 24 hours of operation',
    status: WorkflowStatus.COMPLETED,
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
    completed_at: new Date(Date.now() - 1000 * 60 * 45).toISOString(), // 45 min ago
    current_step: 'release_notes',
    completed_steps: ['bug_analysis', 'bug_fix', 'regression_testing', 'release_notes'],
    files_created: [
      'src/websocket/connection-manager.ts',
      'tests/websocket/connection-manager.spec.ts',
      'docs/CHANGELOG.md'
    ],
    errors: []
  },
  {
    workflow_id: 'workflow_20260114_081245',
    workflow_type: WorkflowType.INFRASTRUCTURE,
    requirement: 'Setup Kubernetes cluster with auto-scaling, load balancing, and monitoring using Prometheus and Grafana',
    status: WorkflowStatus.COMPLETED,
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
    completed_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(), // 3 hours ago
    current_step: 'documentation',
    completed_steps: ['infrastructure_design', 'infrastructure_implementation', 'infrastructure_testing', 'documentation'],
    files_created: [
      'k8s/deployment.yaml',
      'k8s/service.yaml',
      'k8s/hpa.yaml',
      'k8s/ingress.yaml',
      'monitoring/prometheus-config.yaml',
      'monitoring/grafana-dashboard.json',
      'docs/DEPLOYMENT.md',
      'docs/MONITORING.md'
    ],
    errors: []
  },
  {
    workflow_id: 'workflow_20260113_164530',
    workflow_type: WorkflowType.DOCUMENTATION,
    requirement: 'Create comprehensive API documentation with examples, authentication guide, and interactive Swagger UI',
    status: WorkflowStatus.COMPLETED,
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 24 hours ago
    completed_at: new Date(Date.now() - 1000 * 60 * 60 * 22).toISOString(),
    current_step: 'technical_review',
    completed_steps: ['documentation_requirements', 'documentation_creation', 'technical_review'],
    files_created: [
      'docs/API_REFERENCE.md',
      'docs/AUTHENTICATION.md',
      'docs/EXAMPLES.md',
      'swagger.yaml'
    ],
    errors: []
  },
  {
    workflow_id: 'workflow_20260113_142015',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    requirement: 'Implement real-time chat feature with WebSocket, message persistence, file attachments, and emoji support',
    status: WorkflowStatus.FAILED,
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 26).toISOString(),
    current_step: 'qa_testing',
    completed_steps: ['business_analyst', 'architecture_design', 'implementation'],
    files_created: [
      'src/chat/chat.gateway.ts',
      'src/chat/chat.service.ts',
      'src/chat/message.entity.ts'
    ],
    errors: [
      {
        step: 'qa_testing',
        error: 'Test suite failed: WebSocket connection timeout after 30 seconds',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
      }
    ]
  },
  {
    workflow_id: 'workflow_20260113_095520',
    workflow_type: WorkflowType.ANALYSIS,
    requirement: 'Analyze system performance bottlenecks and provide optimization recommendations for database queries',
    status: WorkflowStatus.COMPLETED,
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 60 * 28).toISOString(),
    current_step: 'final_analysis',
    completed_steps: ['requirements_gathering', 'technical_feasibility', 'infrastructure_assessment', 'final_analysis'],
    files_created: [
      'analysis/performance-report.md',
      'analysis/optimization-recommendations.md'
    ],
    errors: []
  }
];

/**
 * Mock Workflow Detail States
 */
export const MOCK_WORKFLOW_STATES: Record<string, WorkflowState> = {
  'workflow_20260114_103022': {
    workflow_id: 'workflow_20260114_103022',
    requirement: 'Create a REST API for user authentication with JWT tokens, OAuth2 integration, and role-based access control',
    workflow_type: 'feature_development',
    status: 'running',
    current_step: 'implementation',
    completed_steps: ['business_analyst', 'architecture_design'],
    business_analysis: [
      {
        summary: 'Requirements analysis completed',
        user_stories: [
          'As a user, I want to register with email and password',
          'As a user, I want to login using OAuth2 providers',
          'As an admin, I want to manage user roles'
        ]
      }
    ],
    architecture: [
      {
        summary: 'System architecture designed',
        components: ['AuthController', 'AuthService', 'JWTStrategy', 'OAuth2Strategy']
      }
    ],
    implementation: [
      {
        summary: 'Implementation in progress',
        status: 'working'
      }
    ],
    files_created: [
      'src/auth/auth.controller.ts',
      'src/auth/auth.service.ts',
      'src/auth/jwt.strategy.ts',
      'src/auth/auth.module.ts',
      'src/auth/dto/login.dto.ts',
      'src/auth/dto/register.dto.ts',
      'src/auth/guards/jwt-auth.guard.ts',
      'src/auth/guards/roles.guard.ts'
    ],
    errors: [],
    started_at: new Date(Date.now() - 1000 * 60 * 30).toISOString()
  },
  'workflow_20260114_093510': {
    workflow_id: 'workflow_20260114_093510',
    requirement: 'Fix memory leak in WebSocket connection handler causing server crashes after 24 hours of operation',
    workflow_type: 'bug_fix',
    status: 'completed',
    current_step: 'release_notes',
    completed_steps: ['bug_analysis', 'bug_fix', 'regression_testing', 'release_notes'],
    files_created: [
      'src/websocket/connection-manager.ts',
      'tests/websocket/connection-manager.spec.ts',
      'docs/CHANGELOG.md'
    ],
    errors: [],
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 45).toISOString()
  },
  'workflow_20260114_081245': {
    workflow_id: 'workflow_20260114_081245',
    requirement: 'Setup Kubernetes cluster with auto-scaling, load balancing, and monitoring using Prometheus and Grafana',
    workflow_type: 'infrastructure',
    status: 'completed',
    current_step: 'documentation',
    completed_steps: ['infrastructure_design', 'infrastructure_implementation', 'infrastructure_testing', 'documentation'],
    files_created: [
      'k8s/deployment.yaml',
      'k8s/service.yaml',
      'k8s/hpa.yaml',
      'k8s/ingress.yaml',
      'monitoring/prometheus-config.yaml',
      'monitoring/grafana-dashboard.json',
      'docs/DEPLOYMENT.md',
      'docs/MONITORING.md'
    ],
    errors: [],
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString()
  }
};

/**
 * Generate random workflow for testing
 */
export function generateRandomWorkflow(): Workflow {
  const types = Object.values(WorkflowType);
  const statuses = Object.values(WorkflowStatus);
  
  return {
    workflow_id: `workflow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    workflow_type: types[Math.floor(Math.random() * types.length)],
    requirement: 'Auto-generated test workflow for UI development',
    status: statuses[Math.floor(Math.random() * statuses.length)],
    started_at: new Date(Date.now() - Math.random() * 1000 * 60 * 60 * 48).toISOString(),
    completed_steps: ['business_analyst'],
    files_created: [],
    errors: []
  };
}
