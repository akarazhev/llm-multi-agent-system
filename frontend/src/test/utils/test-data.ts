import type { Workflow, WorkflowStatus } from '@/types/workflow'
import type { AgentInfo } from '@/types/agent'

// Mock Workflow Data
export const mockWorkflow: Workflow = {
  request_id: 'req-test-1',
  workflow_id: 'wf-test-1',
  requirements: 'Test workflow requirements',
  current_step: 'running',
  status: 'running',
  created_at: '2026-01-13T10:00:00Z',
  updated_at: '2026-01-13T10:05:00Z',
}

export const mockWorkflows: Workflow[] = [
  mockWorkflow,
  {
    request_id: 'req-test-2',
    workflow_id: 'wf-test-2',
    requirements: 'Another test workflow',
    current_step: 'completed',
    status: 'completed',
    created_at: '2026-01-13T09:00:00Z',
    updated_at: '2026-01-13T09:30:00Z',
  },
  {
    request_id: 'req-test-3',
    workflow_id: 'wf-test-3',
    requirements: 'Failed workflow',
    current_step: 'error',
    status: 'failed',
    created_at: '2026-01-13T08:00:00Z',
    updated_at: '2026-01-13T08:15:00Z',
  },
  {
    request_id: 'req-test-4',
    workflow_id: 'wf-test-4',
    requirements: 'Pending workflow',
    current_step: 'initial',
    status: 'pending',
    created_at: '2026-01-13T11:00:00Z',
    updated_at: '2026-01-13T11:00:00Z',
  },
  {
    request_id: 'req-test-5',
    workflow_id: 'wf-test-5',
    requirements: 'Cancelled workflow',
    current_step: 'cancelled',
    status: 'cancelled',
    created_at: '2026-01-13T07:00:00Z',
    updated_at: '2026-01-13T07:10:00Z',
  },
]

// Mock Agent Data
export const mockAgent: AgentInfo = {
  agent_id: 'agent-test-1',
  agent_name: 'Test Agent',
  status: 'active',
  tools: [
    { name: 'test-tool-1', description: 'Test tool 1 description' },
    { name: 'test-tool-2', description: 'Test tool 2 description' },
  ],
  capabilities: ['test', 'development'],
}

export const mockAgents: AgentInfo[] = [
  mockAgent,
  {
    agent_id: 'agent-test-2',
    agent_name: 'Another Test Agent',
    status: 'idle',
    tools: [{ name: 'testing-tool' }],
    capabilities: ['testing'],
  },
  {
    agent_id: 'agent-test-3',
    agent_name: 'Error Agent',
    status: 'error',
    tools: [],
    capabilities: [],
  },
  {
    agent_id: 'agent-test-4',
    agent_name: 'Active Agent',
    status: 'active',
    tools: [
      { name: 'tool-1' },
      { name: 'tool-2' },
      { name: 'tool-3' },
    ],
    capabilities: ['capability-1', 'capability-2'],
  },
]

// Factory functions for creating test data
export const createMockWorkflow = (overrides?: Partial<Workflow>): Workflow => ({
  request_id: `req-${Date.now()}`,
  workflow_id: `wf-${Date.now()}`,
  requirements: 'Test workflow requirements',
  current_step: 'running',
  status: 'running',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  ...overrides,
})

export const createMockAgent = (overrides?: Partial<AgentInfo>): AgentInfo => ({
  agent_id: `agent-${Date.now()}`,
  agent_name: 'Test Agent',
  status: 'active',
  tools: [],
  capabilities: [],
  ...overrides,
})

// Mock data for different workflow statuses
export const mockWorkflowByStatus = (status: WorkflowStatus): Workflow => ({
  request_id: `req-${status}`,
  workflow_id: `wf-${status}`,
  requirements: `Workflow with ${status} status`,
  current_step: status === 'running' ? 'processing' : status === 'completed' ? 'done' : 'initial',
  status,
  created_at: '2026-01-13T10:00:00Z',
  updated_at: '2026-01-13T10:05:00Z',
})

// Mock data for different agent statuses
export const mockAgentByStatus = (status: 'active' | 'idle' | 'error'): AgentInfo => ({
  agent_id: `agent-${status}`,
  agent_name: `${status.charAt(0).toUpperCase() + status.slice(1)} Agent`,
  status,
  tools: status === 'active' ? [{ name: 'active-tool' }] : [],
  capabilities: status === 'active' ? ['capability'] : [],
})
