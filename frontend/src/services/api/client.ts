/**
 * API Client
 * Base configuration and utilities for API calls with retry mechanism
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ApiError {
  message: string;
  status?: number;
  details?: unknown;
}

export class ApiClientError extends Error {
  status?: number;
  details?: unknown;

  constructor(message: string, status?: number, details?: unknown) {
    super(message);
    Object.setPrototypeOf(this, ApiClientError.prototype);
    this.name = 'ApiClientError';
    this.status = status;
    this.details = details;
  }
}

interface RetryOptions {
  maxRetries?: number;
  retryDelay?: number;
  retryableStatuses?: number[];
}

const DEFAULT_RETRY_OPTIONS: Required<RetryOptions> = {
  maxRetries: 3,
  retryDelay: 1000,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
};

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isRetryable(status: number | undefined, retryableStatuses: number[]): boolean {
  if (!status) return true; // Network errors are retryable
  return retryableStatuses.includes(status);
}

/**
 * Base fetch wrapper with error handling and retry mechanism
 */
export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit,
  retryOptions?: RetryOptions
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const retryConfig = { ...DEFAULT_RETRY_OPTIONS, ...retryOptions };
  
  let lastError: Error | null = null;
  
  for (let attempt = 0; attempt <= retryConfig.maxRetries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = new ApiClientError(
          errorData.message || `API request failed: ${response.statusText}`,
          response.status,
          errorData
        );

        // Check if we should retry
        if (
          attempt < retryConfig.maxRetries &&
          isRetryable(response.status, retryConfig.retryableStatuses)
        ) {
          lastError = error;
          await delay(retryConfig.retryDelay * (attempt + 1)); // Exponential backoff
          continue;
        }

        throw error;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiClientError) {
        // If it's not retryable or we've exhausted retries, throw
        if (
          attempt >= retryConfig.maxRetries ||
          !isRetryable(error.status, retryConfig.retryableStatuses)
        ) {
          throw error;
        }
        lastError = error;
        await delay(retryConfig.retryDelay * (attempt + 1));
        continue;
      }

      // Network errors are retryable
      if (attempt < retryConfig.maxRetries) {
        lastError = error instanceof Error ? error : new Error('Unknown error occurred');
        await delay(retryConfig.retryDelay * (attempt + 1));
        continue;
      }

      throw new ApiClientError(
        error instanceof Error ? error.message : 'Unknown error occurred',
        undefined,
        error
      );
    }
  }

  // This should never be reached, but TypeScript needs it
  throw lastError || new ApiClientError('Request failed after retries');
}

/**
 * GET request helper
 */
export function apiGet<T>(endpoint: string, retryOptions?: RetryOptions): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'GET' }, retryOptions);
}

/**
 * POST request helper
 */
export function apiPost<T>(endpoint: string, data?: unknown, retryOptions?: RetryOptions): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  }, retryOptions);
}

/**
 * DELETE request helper
 */
export function apiDelete<T>(endpoint: string, retryOptions?: RetryOptions): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE' }, retryOptions);
}
