import { describe, it, expect } from 'vitest'
import { render, screen } from '@/test/utils/test-utils'
import Input from '@components/atoms/Input'
import { FormField } from './FormField'
import { testAccessibility } from '@/test/utils/accessibility'

describe('FormField', () => {
  it('renders with label and children', () => {
    render(
      <FormField id="test-field" label="Test Label">
        <Input />
      </FormField>
    )
    expect(screen.getByText('Test Label')).toBeInTheDocument()
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('associates label with input via htmlFor', () => {
    render(
      <FormField id="test-field" label="Test Label">
        <Input />
      </FormField>
    )
    const label = screen.getByText('Test Label')
    expect(label).toHaveAttribute('for', 'test-field')
  })

  it('shows required indicator when required is true', () => {
    render(
      <FormField id="test-field" label="Test Label" required>
        <Input />
      </FormField>
    )
    expect(screen.getByText('*')).toBeInTheDocument()
    expect(screen.getByText('*')).toHaveClass('text-destructive')
  })

  it('displays error message when error is true', () => {
    render(
      <FormField
        id="test-field"
        label="Test Label"
        error
        errorMessage="This is an error"
      >
        <Input />
      </FormField>
    )
    expect(screen.getByText('This is an error')).toBeInTheDocument()
    expect(screen.getByText('This is an error')).toHaveAttribute('id', 'test-field-error')
  })

  it('displays helper text when provided', () => {
    render(
      <FormField id="test-field" label="Test Label" helperText="Helper text">
        <Input />
      </FormField>
    )
    expect(screen.getByText('Helper text')).toBeInTheDocument()
  })

  it('prioritizes error message over helper text', () => {
    render(
      <FormField
        id="test-field"
        label="Test Label"
        error
        errorMessage="Error message"
        helperText="Helper text"
      >
        <Input />
      </FormField>
    )
    expect(screen.getByText('Error message')).toBeInTheDocument()
    expect(screen.queryByText('Helper text')).not.toBeInTheDocument()
  })

  it('is accessible', async () => {
    const { container } = render(
      <FormField id="test-field" label="Test Label">
        <Input aria-label="Test Label" />
      </FormField>
    )
    await testAccessibility(container)
  })

  it('renders any children component', () => {
    render(
      <FormField id="test-field" label="Test Label">
        <div data-testid="custom-child">Custom Content</div>
      </FormField>
    )
    expect(screen.getByTestId('custom-child')).toBeInTheDocument()
  })
})
