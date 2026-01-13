import { describe, it, expect } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import { AgentCard } from './AgentCard'
import { mockAgent, createMockAgent } from '@/test/utils/test-data'
import { testAccessibility } from '@/test/utils/accessibility'

describe('AgentCard', () => {
  it('renders agent information', () => {
    render(<AgentCard agent={mockAgent} />)
    expect(screen.getByText(mockAgent.agent_name)).toBeInTheDocument()
    expect(screen.getByText(mockAgent.agent_id)).toBeInTheDocument()
  })

  it('displays status badge', () => {
    render(<AgentCard agent={mockAgent} />)
    expect(screen.getByText('Active')).toBeInTheDocument()
  })

  it('displays tools when available', () => {
    render(<AgentCard agent={mockAgent} />)
    expect(screen.getByText('Tools:')).toBeInTheDocument()
    mockAgent.tools?.forEach((tool) => {
      expect(screen.getByText(tool.name)).toBeInTheDocument()
    })
  })

  it('does not display tools section when tools are empty', () => {
    const agent = createMockAgent({ tools: [] })
    render(<AgentCard agent={agent} />)
    expect(screen.queryByText('Tools:')).not.toBeInTheDocument()
  })

  it('does not display tools section when tools are undefined', () => {
    const agent = createMockAgent({ tools: undefined })
    render(<AgentCard agent={agent} />)
    expect(screen.queryByText('Tools:')).not.toBeInTheDocument()
  })

  it('handles different agent statuses', () => {
    const statuses = ['active', 'idle', 'error'] as const
    statuses.forEach((status) => {
      const { unmount } = render(
        <AgentCard agent={createMockAgent({ status })} />
      )
      expect(screen.getByText(new RegExp(status, 'i'))).toBeInTheDocument()
      unmount()
    })
  })

  it('displays multiple tools correctly', () => {
    const agent = createMockAgent({
      tools: [
        { name: 'tool-1' },
        { name: 'tool-2' },
        { name: 'tool-3' },
      ],
    })
    render(<AgentCard agent={agent} />)
    expect(screen.getByText('tool-1')).toBeInTheDocument()
    expect(screen.getByText('tool-2')).toBeInTheDocument()
    expect(screen.getByText('tool-3')).toBeInTheDocument()
  })

  it('is accessible', async () => {
    const { container } = render(<AgentCard agent={mockAgent} />)
    await testAccessibility(container)
  })

  it('renders agent name and ID correctly', () => {
    const agent = createMockAgent({
      agent_name: 'Custom Agent Name',
      agent_id: 'custom-agent-id',
    })
    render(<AgentCard agent={agent} />)
    expect(screen.getByText('Custom Agent Name')).toBeInTheDocument()
    expect(screen.getByText('custom-agent-id')).toBeInTheDocument()
  })
})
