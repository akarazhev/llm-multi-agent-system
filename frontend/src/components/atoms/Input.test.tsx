import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import userEvent from '@testing-library/user-event'
import Input from './Input'
import { testAccessibility } from '@/test/utils/accessibility'

describe('Input', () => {
  it('renders with default props', () => {
    render(<Input />)
    const input = screen.getByRole('textbox')
    expect(input).toBeInTheDocument()
  })

  it('renders with placeholder', () => {
    render(<Input placeholder="Enter text" />)
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()
  })

  it('handles value changes', async () => {
    const user = userEvent.setup()
    render(<Input />)
    const input = screen.getByRole('textbox') as HTMLInputElement
    
    await user.type(input, 'test value')
    expect(input.value).toBe('test value')
  })

  it('displays helper text', () => {
    render(<Input helperText="This is helper text" />)
    expect(screen.getByText('This is helper text')).toBeInTheDocument()
    expect(screen.getByText('This is helper text')).toHaveAttribute('id', 'helper-text')
  })

  it('displays error message when error is true', () => {
    render(<Input error errorMessage="This is an error" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(screen.getByText('This is an error')).toBeInTheDocument()
    expect(screen.getByText('This is an error')).toHaveAttribute('id', 'error-message')
    expect(screen.getByText('This is an error')).toHaveAttribute('role', 'alert')
  })

  it('applies error styles when error is true', () => {
    render(<Input error />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveClass('border-error')
  })

  it('does not show helper text when error is present', () => {
    render(<Input error errorMessage="Error" helperText="Helper" />)
    expect(screen.queryByText('Helper')).not.toBeInTheDocument()
    expect(screen.getByText('Error')).toBeInTheDocument()
  })

  it('is disabled when disabled prop is true', () => {
    render(<Input disabled />)
    const input = screen.getByRole('textbox')
    expect(input).toBeDisabled()
  })

  it('supports different input types', () => {
    const { rerender } = render(<Input type="text" />)
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'text')

    rerender(<Input type="email" />)
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'email')
  })

  it('forwards ref correctly', () => {
    const ref = vi.fn()
    render(<Input ref={ref} />)
    expect(ref).toHaveBeenCalled()
  })

  it('applies custom className', () => {
    render(<Input className="custom-class" />)
    expect(screen.getByRole('textbox')).toHaveClass('custom-class')
  })

  it('is accessible', async () => {
    const { container } = render(<Input aria-label="Test input" />)
    await testAccessibility(container)
  })

  it('has proper ARIA attributes when error', () => {
    render(<Input error errorMessage="Error message" aria-label="Test" />)
    const input = screen.getByLabelText('Test')
    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(input).toHaveAttribute('aria-describedby', 'error-message')
  })

  it('has proper ARIA attributes when helper text', () => {
    render(<Input helperText="Helper text" aria-label="Test" />)
    const input = screen.getByLabelText('Test')
    expect(input).toHaveAttribute('aria-describedby', 'helper-text')
  })
})
