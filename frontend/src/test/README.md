# Testing Infrastructure

This directory contains all testing utilities, mocks, and test files for the frontend application.

## Structure

```
src/test/
├── setup.ts              # Test setup and configuration
├── mocks/                # MSW handlers and server setup
│   ├── handlers.ts       # API mock handlers
│   └── server.ts        # MSW server configuration
├── utils/                # Testing utilities
│   ├── test-utils.tsx    # Custom render with providers
│   ├── test-data.ts      # Mock data factories
│   └── accessibility.ts  # Accessibility testing helpers
└── e2e/                  # End-to-end tests (Playwright)
    └── example.spec.ts   # Example E2E test
```

## Running Tests

### Unit/Component Tests (Vitest)
```bash
npm run test              # Run tests once
npm run test:watch        # Run tests in watch mode
npm run test:ui           # Run tests with UI
npm run test:coverage     # Run tests with coverage report
```

### E2E Tests (Playwright)
```bash
npm run test:e2e         # Run E2E tests
npm run test:e2e:ui      # Run E2E tests with UI
```

## Testing Utilities

### Custom Render
Use `render` from `@/test/utils/test-utils` instead of `@testing-library/react` to get automatic providers:

```tsx
import { render, screen } from '@/test/utils/test-utils'
import { MyComponent } from '@/components/MyComponent'

test('renders component', () => {
  render(<MyComponent />)
  expect(screen.getByText('Hello')).toBeInTheDocument()
})
```

### Mock Data
Use mock data factories from `@/test/utils/test-data`:

```tsx
import { mockWorkflow, mockAgents } from '@/test/utils/test-data'
```

### Accessibility Testing
Use accessibility helpers from `@/test/utils/accessibility`:

```tsx
import { testAccessibility } from '@/test/utils/accessibility'

test('component is accessible', async () => {
  const { container } = render(<MyComponent />)
  await testAccessibility(container)
})
```

## MSW (Mock Service Worker)

API mocking is set up using MSW. Handlers are defined in `mocks/handlers.ts` and automatically used in tests.

## Coverage Goals

- **Minimum**: 80% overall coverage
- **Critical paths**: 90%+ (API client, state management, workflow management)
- **UI components**: 70%+ (some visual components are hard to test meaningfully)

## Test Organization

- **Unit tests**: Co-located with components (e.g., `components/Button/Button.test.tsx`)
- **Integration tests**: In `src/test/integration/`
- **E2E tests**: In `src/test/e2e/`
