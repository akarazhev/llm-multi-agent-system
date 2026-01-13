/**
 * MSW Browser Setup
 * For development mode with mock API
 */

import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

// This configures a request mocking server for the browser
export const worker = setupWorker(...handlers);
