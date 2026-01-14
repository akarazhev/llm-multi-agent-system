import { Injectable, signal, inject } from '@angular/core';
import { Subject } from 'rxjs';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../../../environments/environment';

export interface WorkflowWsMessage {
  event_type: string;
  workflow_id: string;
  data: Record<string, unknown>;
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private readonly keycloak = inject(KeycloakService);
  private socket?: WebSocket;
  private messageSubject = new Subject<WorkflowWsMessage>();
  readonly messages$ = this.messageSubject.asObservable();
  readonly connectionStatus = signal<'connected' | 'disconnected' | 'connecting'>('disconnected');

  async connect(workflowId: string): Promise<void> {
    if (!environment.wsUrl) {
      return;
    }

    if (this.socket) {
      this.socket.close();
    }

    this.connectionStatus.set('connecting');
    const token = environment.authEnabled ? await this.keycloak.getToken() : undefined;
    const url = token
      ? `${environment.wsUrl}/workflows/${workflowId}?token=${encodeURIComponent(token)}`
      : `${environment.wsUrl}/workflows/${workflowId}`;

    this.socket = new WebSocket(url);
    this.socket.onopen = () => this.connectionStatus.set('connected');
    this.socket.onclose = () => this.connectionStatus.set('disconnected');
    this.socket.onerror = () => this.connectionStatus.set('disconnected');
    this.socket.onmessage = (event) => {
      try {
        this.messageSubject.next(JSON.parse(event.data));
      } catch {
        return;
      }
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = undefined;
      this.connectionStatus.set('disconnected');
    }
  }
}
