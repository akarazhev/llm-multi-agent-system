import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  Workflow, 
  WorkflowCreateRequest, 
  WorkflowState 
} from '../../core/interfaces/workflow.interface';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WorkflowService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  /**
   * Get all workflows
   */
  getWorkflows(): Observable<Workflow[]> {
    return this.http.get<Workflow[]>(`${this.apiUrl}/workflows`);
  }

  /**
   * Get workflow by ID
   */
  getWorkflow(workflowId: string): Observable<WorkflowState> {
    return this.http.get<WorkflowState>(`${this.apiUrl}/workflows/${workflowId}`);
  }

  /**
   * Create new workflow
   */
  createWorkflow(request: WorkflowCreateRequest): Observable<Workflow> {
    return this.http.post<Workflow>(`${this.apiUrl}/workflows`, request);
  }

  /**
   * Cancel workflow
   */
  cancelWorkflow(workflowId: string): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}/workflows/${workflowId}/cancel`, {});
  }

  /**
   * Get workflow results/output
   */
  getWorkflowResults(workflowId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/workflows/${workflowId}/results`);
  }

  /**
   * Resume workflow
   */
  resumeWorkflow(workflowId: string): Observable<Workflow> {
    return this.http.post<Workflow>(`${this.apiUrl}/workflows/${workflowId}/resume`, {});
  }
}
