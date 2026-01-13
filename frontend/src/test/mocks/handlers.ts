import { http, HttpResponse } from 'msw'
import type { Workflow } from '@/types/workflow'
import type { AgentInfo } from '@/types/agent'
import { mockWorkflows, mockAgents, createMockWorkflow } from '@/test/utils/test-data'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const handlers = [
  // Health check
  http.get(`${API_BASE_URL}/health`, () => {
    return HttpResponse.json({ status: 'ok' })
  }),

  // Get workflows
  http.get(`${API_BASE_URL}/api/workflows`, () => {
    return HttpResponse.json(mockWorkflows)
  }),

  // Get workflow by ID
  http.get(`${API_BASE_URL}/api/workflows/:id`, ({ params }) => {
    const workflow = mockWorkflows.find(
      (w) => w.request_id === params.id || w.workflow_id === params.id
    )
    if (workflow) {
      return HttpResponse.json(workflow)
    }
    return HttpResponse.json(
      { error: 'Workflow not found' },
      { status: 404 }
    )
  }),

  // Create workflow
  http.post(`${API_BASE_URL}/api/workflows`, async ({ request }) => {
    const body = await request.json()
    const newWorkflow = createMockWorkflow({
      requirements: (body as { requirements: string }).requirements || 'New workflow',
      status: 'pending',
      current_step: 'initial',
    })
    return HttpResponse.json(newWorkflow, { status: 201 })
  }),

  // Cancel workflow
  http.post(`${API_BASE_URL}/api/workflows/:id/cancel`, ({ params }) => {
    const workflow = mockWorkflows.find(
      (w) => w.request_id === params.id || w.workflow_id === params.id
    )
    if (workflow) {
      return HttpResponse.json({
        ...workflow,
        status: 'cancelled',
        updated_at: new Date().toISOString(),
      })
    }
    return HttpResponse.json(
      { error: 'Workflow not found' },
      { status: 404 }
    )
  }),

  // Get agents
  http.get(`${API_BASE_URL}/api/agents`, () => {
    return HttpResponse.json(mockAgents)
  }),

  // Get agent by ID
  http.get(`${API_BASE_URL}/api/agents/:id`, ({ params }) => {
    const agent = mockAgents.find((a) => a.agent_id === params.id)
    if (agent) {
      return HttpResponse.json(agent)
    }
    return HttpResponse.json(
      { error: 'Agent not found' },
      { status: 404 }
    )
  }),
]
