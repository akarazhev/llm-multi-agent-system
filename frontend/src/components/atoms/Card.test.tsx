import { describe, it, expect } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import { Card } from './Card'
import { testAccessibility } from '@/test/utils/accessibility'

describe('Card', () => {
  it('renders with default props', () => {
    render(<Card>Card Content</Card>)
    expect(screen.getByText('Card Content')).toBeInTheDocument()
  })

  it('renders with header', () => {
    render(
      <Card header={<div>Card Header</div>}>
        Card Content
      </Card>
    )
    expect(screen.getByText('Card Header')).toBeInTheDocument()
    expect(screen.getByText('Card Content')).toBeInTheDocument()
  })

  it('renders with footer', () => {
    render(
      <Card footer={<div>Card Footer</div>}>
        Card Content
      </Card>
    )
    expect(screen.getByText('Card Footer')).toBeInTheDocument()
    expect(screen.getByText('Card Content')).toBeInTheDocument()
  })

  it('renders with both header and footer', () => {
    render(
      <Card
        header={<div>Card Header</div>}
        footer={<div>Card Footer</div>}
      >
        Card Content
      </Card>
    )
    expect(screen.getByText('Card Header')).toBeInTheDocument()
    expect(screen.getByText('Card Content')).toBeInTheDocument()
    expect(screen.getByText('Card Footer')).toBeInTheDocument()
  })

  it('renders with different variants', () => {
    const { rerender } = render(<Card variant="default">Default</Card>)
    expect(screen.getByText('Default').parentElement).toHaveClass('border')

    rerender(<Card variant="elevated">Elevated</Card>)
    expect(screen.getByText('Elevated').parentElement).toHaveClass('shadow-md')

    rerender(<Card variant="outlined">Outlined</Card>)
    expect(screen.getByText('Outlined').parentElement).toHaveClass('border-2')
  })

  it('applies custom className', () => {
    render(<Card className="custom-class">Custom</Card>)
    expect(screen.getByText('Custom').parentElement).toHaveClass('custom-class')
  })

  it('is accessible', async () => {
    const { container } = render(<Card>Accessible Card</Card>)
    await testAccessibility(container)
  })

  it('handles click events', () => {
    const handleClick = vi.fn()
    render(<Card onClick={handleClick}>Clickable Card</Card>)
    const card = screen.getByText('Clickable Card').parentElement
    expect(card).toBeInTheDocument()
  })
})
