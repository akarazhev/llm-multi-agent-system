import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AgentMessage, CommunicationStats, MessageThread } from '../../core/interfaces/agent-message.interface';

@Injectable({
  providedIn: 'root'
})
export class CommunicationService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  getMessages(workflowId: string) {
    return this.http.get<AgentMessage[]>(`${this.apiUrl}/communication/${workflowId}/messages`).pipe(
      catchError(() => of([]))
    );
  }

  getThreads(workflowId: string) {
    return this.http.get<MessageThread[]>(`${this.apiUrl}/communication/${workflowId}/threads`).pipe(
      catchError(() => of([]))
    );
  }

  getStats(workflowId: string) {
    return this.http.get<CommunicationStats>(`${this.apiUrl}/communication/${workflowId}/stats`).pipe(
      catchError(() => of({
        total_messages: 0,
        messages_by_type: {},
        messages_by_agent: {},
        threads_count: 0,
        open_threads: 0,
        resolved_threads: 0,
        decisions_count: 0,
        average_response_time_seconds: 0
      }))
    );
  }
}
