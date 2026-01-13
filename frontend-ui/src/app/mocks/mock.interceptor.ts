import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { of, delay } from 'rxjs';
import { MOCK_AGENTS, MOCK_WORKFLOWS, MOCK_WORKFLOW_STATES } from './mock-data';

/**
 * HTTP Interceptor for mocking API responses
 */
export const mockInterceptor: HttpInterceptorFn = (req, next) => {
  const url = req.url;

  // Simulate network delay
  const MOCK_DELAY = 500; // ms

  // Mock GET /api/agents
  if (url.includes('/api/agents') && req.method === 'GET' && !url.includes('/status')) {
    console.log('🎭 [MOCK] GET /api/agents');
    return of(new HttpResponse({
      status: 200,
      body: MOCK_AGENTS
    })).pipe(delay(MOCK_DELAY));
  }

  // Mock GET /api/agents/{id}
  if (url.match(/\/api\/agents\/[\w-]+$/) && req.method === 'GET') {
    const agentId = url.split('/').pop();
    const agent = MOCK_AGENTS.find(a => a.agent_id === agentId);
    console.log(`🎭 [MOCK] GET /api/agents/${agentId}`);
    
    if (agent) {
      return of(new HttpResponse({
        status: 200,
        body: agent
      })).pipe(delay(MOCK_DELAY));
    } else {
      return of(new HttpResponse({
        status: 404,
        body: { error: 'Agent not found' }
      })).pipe(delay(MOCK_DELAY));
    }
  }

  // Mock GET /api/workflows
  if (url.includes('/api/workflows') && req.method === 'GET' && !url.match(/\/api\/workflows\/[\w-]+/)) {
    console.log('🎭 [MOCK] GET /api/workflows');
    return of(new HttpResponse({
      status: 200,
      body: MOCK_WORKFLOWS
    })).pipe(delay(MOCK_DELAY));
  }

  // Mock GET /api/workflows/{id}
  if (url.match(/\/api\/workflows\/[\w-]+$/) && req.method === 'GET') {
    const workflowId = url.split('/').pop();
    console.log(`🎭 [MOCK] GET /api/workflows/${workflowId}`);
    
    const workflowState = MOCK_WORKFLOW_STATES[workflowId as string];
    
    if (workflowState) {
      return of(new HttpResponse({
        status: 200,
        body: workflowState
      })).pipe(delay(MOCK_DELAY));
    } else {
      // Return basic workflow info if detailed state not available
      const workflow = MOCK_WORKFLOWS.find(w => w.workflow_id === workflowId);
      if (workflow) {
        return of(new HttpResponse({
          status: 200,
          body: {
            ...workflow,
            business_analysis: [],
            architecture: [],
            implementation: [],
            tests: [],
            infrastructure: [],
            documentation: []
          }
        })).pipe(delay(MOCK_DELAY));
      } else {
        return of(new HttpResponse({
          status: 404,
          body: { error: 'Workflow not found' }
        })).pipe(delay(MOCK_DELAY));
      }
    }
  }

  // Mock POST /api/workflows (create workflow)
  if (url.includes('/api/workflows') && req.method === 'POST' && !url.includes('/cancel') && !url.includes('/resume')) {
    console.log('🎭 [MOCK] POST /api/workflows');
    const body = req.body as any;
    const newWorkflow = {
      workflow_id: `workflow_${Date.now()}`,
      workflow_type: body?.workflow_type || 'feature_development',
      requirement: body?.requirement || 'New workflow',
      status: 'pending',
      started_at: new Date().toISOString(),
      completed_steps: [],
      files_created: [],
      errors: []
    };
    
    return of(new HttpResponse({
      status: 201,
      body: newWorkflow
    })).pipe(delay(MOCK_DELAY));
  }

  // Mock POST /api/workflows/{id}/cancel
  if (url.includes('/cancel') && req.method === 'POST') {
    console.log('🎭 [MOCK] POST /api/workflows/{id}/cancel');
    return of(new HttpResponse({
      status: 200,
      body: { message: 'Workflow cancelled successfully' }
    })).pipe(delay(MOCK_DELAY));
  }

  // Mock POST /api/workflows/{id}/resume
  if (url.includes('/resume') && req.method === 'POST') {
    console.log('🎭 [MOCK] POST /api/workflows/{id}/resume');
    return of(new HttpResponse({
      status: 200,
      body: { message: 'Workflow resumed successfully' }
    })).pipe(delay(MOCK_DELAY));
  }

  // Pass through if not mocked
  return next(req);
};
