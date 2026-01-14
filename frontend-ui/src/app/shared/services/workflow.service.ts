import { Injectable, signal, computed, OnDestroy, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, finalize, of, tap } from 'rxjs';
import {
  Workflow,
  WorkflowTemplate,
  WorkflowStatus,
  WorkflowType,
  WorkflowPriority,
  WorkflowCreateRequest
} from '../../core/interfaces/workflow.interface';
import { WORKFLOW_TEMPLATES } from '../../mocks/mock-workflows';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WorkflowService implements OnDestroy {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;
  private workflows = signal<Workflow[]>([]);
  private templates = signal<WorkflowTemplate[]>([...WORKFLOW_TEMPLATES]);
  private loading = signal<boolean>(false);
  private autoRefreshInterval: any = null;
  private autoRefreshEnabled = signal<boolean>(false);

  // Public read-only signals
  readonly workflowsSignal = this.workflows.asReadonly();
  readonly templatesSignal = this.templates.asReadonly();
  readonly loadingSignal = this.loading.asReadonly();

  // Computed signals
  readonly runningWorkflows = computed(() =>
    this.workflows().filter(w => w.status === WorkflowStatus.RUNNING)
  );

  readonly completedWorkflows = computed(() =>
    this.workflows().filter(w => w.status === WorkflowStatus.COMPLETED)
  );

  readonly failedWorkflows = computed(() =>
    this.workflows().filter(w => w.status === WorkflowStatus.FAILED)
  );

  readonly workflowsByProject = computed(() => {
    const byProject = new Map<string, Workflow[]>();
    this.workflows().forEach(workflow => {
      if (workflow.project_id) {
        const existing = byProject.get(workflow.project_id) || [];
        byProject.set(workflow.project_id, [...existing, workflow]);
      }
    });
    return byProject;
  });

  readonly totalWorkflows = computed(() => this.workflows().length);
  readonly runningCount = computed(() => this.runningWorkflows().length);
  readonly completedCount = computed(() => this.completedWorkflows().length);
  readonly failedCount = computed(() => this.failedWorkflows().length);

  constructor() {
    this.loadWorkflows();
  }

  /**
   * Load all workflows from backend (simulated with mock data)
   */
  loadWorkflows(): void {
    this.loading.set(true);
    this.http.get<Workflow[]>(`${this.apiUrl}/workflows`).pipe(
      catchError(() => of([])),
      finalize(() => this.loading.set(false))
    ).subscribe(workflows => this.workflows.set(workflows));
  }

  /**
   * Get workflow by ID
   */
  getWorkflowById(id: string) {
    return this.http.get<Workflow>(`${this.apiUrl}/workflows/${id}`).pipe(
      catchError(() => of(undefined))
    );
  }

  /**
   * Get workflows by project ID
   */
  getWorkflowsByProject(projectId: string): Workflow[] {
    return this.workflows().filter(w => w.project_id === projectId);
  }

  /**
   * Get workflows by status
   */
  getWorkflowsByStatus(status: WorkflowStatus): Workflow[] {
    return this.workflows().filter(w => w.status === status);
  }

  /**
   * Get workflows by type
   */
  getWorkflowsByType(type: WorkflowType): Workflow[] {
    return this.workflows().filter(w => w.workflow_type === type);
  }

  /**
   * Get template by ID
   */
  getTemplateById(id: string): WorkflowTemplate | undefined {
    return this.templates().find(t => t.template_id === id);
  }

  /**
   * Create a new workflow
   */
  createWorkflow(request: WorkflowCreateRequest) {
    return this.http.post<Workflow>(`${this.apiUrl}/workflows`, request).pipe(
      tap(workflow => this.workflows.update(workflows => [...workflows, workflow])),
      catchError(() => of(undefined))
    );
  }

  /**
   * Update workflow
   */
  updateWorkflow(workflowId: string, updates: Partial<Workflow>): void {
    this.workflows.update(workflows =>
      workflows.map(w => w.workflow_id === workflowId ? { ...w, ...updates } : w)
    );
  }

  /**
   * Delete workflow
   */
  deleteWorkflow(workflowId: string): void {
    this.http.delete(`${this.apiUrl}/workflows/${workflowId}`).pipe(
      catchError(() => of(null))
    ).subscribe(() => {
      this.workflows.update(workflows => workflows.filter(w => w.workflow_id !== workflowId));
    });
  }

  /**
   * Cancel workflow
   */
  cancelWorkflow(workflowId: string): void {
    this.http.post<Workflow>(`${this.apiUrl}/workflows/${workflowId}/cancel`, {}).pipe(
      catchError(() => of(undefined))
    ).subscribe(workflow => {
      if (workflow) {
        this.updateWorkflow(workflowId, workflow);
      }
    });
  }

  /**
   * Get workflow type display name
   */
  getTypeDisplayName(type: WorkflowType): string {
    const names: Record<WorkflowType, string> = {
      [WorkflowType.FEATURE_DEVELOPMENT]: 'Feature Development',
      [WorkflowType.BUG_FIX]: 'Bug Fix',
      [WorkflowType.INFRASTRUCTURE]: 'Infrastructure',
      [WorkflowType.DOCUMENTATION]: 'Documentation',
      [WorkflowType.ANALYSIS]: 'Analysis',
      [WorkflowType.CODE_REVIEW]: 'Code Review',
      [WorkflowType.TESTING]: 'Testing',
      [WorkflowType.DEPLOYMENT]: 'Deployment',
      [WorkflowType.REFACTORING]: 'Refactoring'
    };
    return names[type] || type;
  }

  /**
   * Get workflow type icon
   */
  getTypeIcon(type: WorkflowType): string {
    const icons: Record<WorkflowType, string> = {
      [WorkflowType.FEATURE_DEVELOPMENT]: 'rocket_launch',
      [WorkflowType.BUG_FIX]: 'bug_report',
      [WorkflowType.INFRASTRUCTURE]: 'cloud',
      [WorkflowType.DOCUMENTATION]: 'description',
      [WorkflowType.ANALYSIS]: 'analytics',
      [WorkflowType.CODE_REVIEW]: 'rate_review',
      [WorkflowType.TESTING]: 'science',
      [WorkflowType.DEPLOYMENT]: 'publish',
      [WorkflowType.REFACTORING]: 'build'
    };
    return icons[type] || 'account_tree';
  }

  /**
   * Get priority color
   */
  getPriorityColor(priority: WorkflowPriority): 'primary' | 'accent' | 'warn' {
    switch (priority) {
      case WorkflowPriority.CRITICAL:
        return 'warn';
      case WorkflowPriority.HIGH:
        return 'accent';
      default:
        return 'primary';
    }
  }

  /**
   * Enable auto-refresh for running workflows
   */
  enableAutoRefresh(intervalMs: number = 5000): void {
    if (this.autoRefreshInterval) {
      return; // Already enabled
    }
    this.autoRefreshEnabled.set(true);
    this.autoRefreshInterval = setInterval(() => {
      this.loadWorkflows();
    }, intervalMs);
  }

  /**
   * Disable auto-refresh
   */
  disableAutoRefresh(): void {
    if (this.autoRefreshInterval) {
      clearInterval(this.autoRefreshInterval);
      this.autoRefreshInterval = null;
      this.autoRefreshEnabled.set(false);
    }
  }

  /**
   * Check if auto-refresh is enabled
   */
  isAutoRefreshEnabled(): boolean {
    return this.autoRefreshEnabled();
  }

  ngOnDestroy(): void {
    this.disableAutoRefresh();
  }
}
