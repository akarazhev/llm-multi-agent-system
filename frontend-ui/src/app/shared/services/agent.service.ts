import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Agent } from '../../core/interfaces/agent.interface';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  /**
   * Get all agents status
   */
  getAgents(): Observable<Agent[]> {
    return this.http.get<Agent[]>(`${this.apiUrl}/agents`);
  }

  /**
   * Get specific agent details
   */
  getAgent(agentId: string): Observable<Agent> {
    return this.http.get<Agent>(`${this.apiUrl}/agents/${agentId}`);
  }

  /**
   * Get agent status
   */
  getAgentStatus(agentId: string): Observable<Agent> {
    return this.http.get<Agent>(`${this.apiUrl}/agents/${agentId}/status`);
  }
}
