import { axe, toHaveNoViolations } from 'jest-axe'
import { expect } from 'vitest'

// Extend Vitest's expect with axe matchers
expect.extend(toHaveNoViolations)

/**
 * Test accessibility of a rendered component
 * @param container - The container element to test
 * @returns Promise that resolves when accessibility check is complete
 */
export async function testAccessibility(container: HTMLElement) {
  const results = await axe(container)
  expect(results).toHaveNoViolations()
}
