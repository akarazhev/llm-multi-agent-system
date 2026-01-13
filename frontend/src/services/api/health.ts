/**
 * Health Check API Service
 */

import { apiGet } from './client';

export interface HealthCheckResponse {
  status: string;
  message?: string;
}

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
  return apiGet<HealthCheckResponse>('/health');
}
