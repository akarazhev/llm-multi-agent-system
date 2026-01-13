import { describe, it, expect } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import { StatusBadge } from './StatusBadge'
import { testAccessibility } from '@/test/utils/accessibility'

describe('StatusBadge', () => {
  it('renders with workflow status', () => {
    render(<StatusBadge status="pending" type="workflow" />)
    expect(screen.getByText('Pending')).toBeInTheDocument()
  })

  it('renders correct variant for workflow statuses', () => {
    const { rerender } = render(<StatusBadge status="pending" type="workflow" />)
    expect(screen.getByText('Pending')).toHaveClass('bg-secondary')

    rerender(<StatusBadge status="running" type="workflow" />)
    expect(screen.getByText('Running')).toHaveClass('bg-secondary')

    rerender(<StatusBadge status="completed" type="workflow" />)
    expect(screen.getByText('Completed')).toHaveClass('bg-success')

    rerender(<StatusBadge status="failed" type="workflow" />)
    expect(screen.getByText('Failed')).toHaveClass('bg-error')

    rerender(<StatusBadge status="cancelled" type="workflow" />)
    expect(screen.getByText('Cancelled')).toHaveClass('bg-secondary')
  })

  it('renders correct variant for agent statuses', () => {
    const { rerender } = render(<StatusBadge status="active" type="agent" />)
    expect(screen.getByText('Active')).toHaveClass('bg-success')

    rerender(<StatusBadge status="idle" type="agent" />)
    expect(screen.getByText('Idle')).toHaveClass('bg-secondary')

    rerender(<StatusBadge status="error" type="agent" />)
    expect(screen.getByText('Error')).toHaveClass('bg-error')
  })

  it('handles unknown status gracefully', () => {
    render(<StatusBadge status="unknown" as any type="workflow" />)
    expect(screen.getByText('unknown')).toBeInTheDocument()
  })

  it('is accessible', async () => {
    const { container } = render(<StatusBadge status="active" type="agent" />)
    await testAccessibility(container)
  })

  it('works without type prop', () => {
    render(<StatusBadge status="pending" />)
    expect(screen.getByText('Pending')).toBeInTheDocument()
  })
})
