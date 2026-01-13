import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import userEvent from '@testing-library/user-event'
import { WorkflowCard } from './WorkflowCard'
import { mockWorkflow, createMockWorkflow } from '@/test/utils/test-data'
import { testAccessibility } from '@/test/utils/accessibility'

describe('WorkflowCard', () => {
  it('renders workflow information', () => {
    render(<WorkflowCard workflow={mockWorkflow} />)
    expect(screen.getByText(mockWorkflow.request_id)).toBeInTheDocument()
    expect(screen.getByText(mockWorkflow.workflow_id)).toBeInTheDocument()
  })

  it('displays status badge', () => {
    render(<WorkflowCard workflow={mockWorkflow} />)
    expect(screen.getByText('Running')).toBeInTheDocument()
  })

  it('displays current step when available', () => {
    render(<WorkflowCard workflow={mockWorkflow} />)
    expect(screen.getByText(mockWorkflow.current_step!)).toBeInTheDocument()
  })

  it('calls onCancel when cancel button is clicked', async () => {
    const handleCancel = vi.fn()
    const workflow = createMockWorkflow({ status: 'running' })
    const user = userEvent.setup()
    
    render(<WorkflowCard workflow={workflow} onCancel={handleCancel} />)
    
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
    await user.click(buttons[1])
    
    expect(handleCancel).toHaveBeenCalledWith(workflow.workflow_id)
  })

  it('shows cancel button for pending workflow', () => {
    const workflow = createMockWorkflow({ status: 'pending' })
    render(<WorkflowCard workflow={workflow} onCancel={vi.fn()} />)
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
  })

  it('shows cancel button for running workflow', () => {
    const workflow = createMockWorkflow({ status: 'running' })
    render(<WorkflowCard workflow={workflow} onCancel={vi.fn()} />)
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
  })

  it('does not show cancel button for completed workflow', () => {
    const workflow = createMockWorkflow({ status: 'completed' })
    render(<WorkflowCard workflow={workflow} onCancel={vi.fn()} />)
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(1)
  })

  it('does not show cancel button when onCancel is not provided', () => {
    render(<WorkflowCard workflow={mockWorkflow} />)
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(1)
  })

  it('displays message when available', () => {
    const workflow = createMockWorkflow({ message: 'Test message' })
    render(<WorkflowCard workflow={workflow} />)
    expect(screen.getByText('Test message')).toBeInTheDocument()
  })

  it('is accessible', async () => {
    const { container } = render(<WorkflowCard workflow={mockWorkflow} />)
    await testAccessibility(container)
  })

  it('handles different workflow statuses', () => {
    const statuses = ['pending', 'running', 'completed', 'failed', 'cancelled'] as const
    statuses.forEach((status) => {
      const { unmount } = render(
        <WorkflowCard workflow={createMockWorkflow({ status })} />
      )
      const statusText = status.charAt(0).toUpperCase() + status.slice(1)
      const statusElements = screen.getAllByText(statusText)
      expect(statusElements.length).toBeGreaterThan(0)
      unmount()
    })
  })
})
