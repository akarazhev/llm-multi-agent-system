import { WorkflowState } from '../core/interfaces/workflow.interface';

// Export from centralized mock files
export { MOCK_AGENTS, AGENT_TEMPLATES } from './mock-agents';
export { MOCK_WORKFLOWS, WORKFLOW_TEMPLATES } from './mock-workflows';

/**
 * Mock Workflow Detail States (legacy format - to be migrated)
 */
export const MOCK_WORKFLOW_STATES: Record<string, WorkflowState> = {
  'wf_20260114_001': {
    workflow_id: 'wf_20260114_001',
    requirement: 'Add user authentication with JWT tokens, refresh token rotation, and secure session management',
    workflow_type: 'feature_development',
    status: 'running',
    current_step: 'Implementation',
    completed_steps: ['Requirements Analysis', 'Architecture Design'],
    business_analysis: [
      {
        summary: 'Requirements documented: JWT with 15min access tokens, 7-day refresh tokens, secure httpOnly cookies',
        user_stories: [
          'As a user, I want to login with email and password',
          'As a user, I want my session to remain active without re-login',
          'As a system, I want to securely manage authentication tokens'
        ]
      }
    ],
    architecture: [
      {
        summary: 'Architecture designed with interceptor-based token refresh and secure storage',
        components: ['AuthService', 'JWTInterceptor', 'AuthGuard', 'TokenStorage']
      }
    ],
    implementation: [
      {
        summary: 'Implementation in progress',
        status: 'working'
      }
    ],
    files_created: [
      'auth.service.ts',
      'jwt.interceptor.ts',
      'auth.guard.ts'
    ],
    errors: [],
    started_at: '2026-01-14T10:30:00Z'
  }
};
