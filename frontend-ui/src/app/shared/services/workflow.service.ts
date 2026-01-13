import { Injectable, signal, computed } from '@angular/core';
import {
  Workflow,
  WorkflowTemplate,
  WorkflowStatus,
  WorkflowType,
  WorkflowPriority,
  WorkflowCreateRequest
} from '../../core/interfaces/workflow.interface';
import { MOCK_WORKFLOWS, WORKFLOW_TEMPLATES } from '../../mocks/mock-workflows';

@Injectable({
  providedIn: 'root'
})
export class WorkflowService {
  private workflows = signal<Workflow[]>([...MOCK_WORKFLOWS]);
  private templates = signal<WorkflowTemplate[]>([...WORKFLOW_TEMPLATES]);
  private loading = signal<boolean>(false);

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
    // Simulate API call
    setTimeout(() => {
      this.workflows.set([...MOCK_WORKFLOWS]);
      this.loading.set(false);
    }, 500);
  }

  /**
   * Get workflow by ID
   */
  getWorkflowById(id: string): Workflow | undefined {
    return this.workflows().find(w => w.workflow_id === id);
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
  createWorkflow(request: WorkflowCreateRequest): Workflow {
    const template = request.workflow_type
      ? this.templates().find(t => t.workflow_type === request.workflow_type)
      : undefined;

    const newWorkflow: Workflow = {
      workflow_id: `wf_${Date.now()}`,
      name: request.name,
      description: request.description || '',
      workflow_type: request.workflow_type,
      requirement: request.requirement,
      status: WorkflowStatus.PENDING,
      started_at: new Date().toISOString(),
      completed_steps: [],
      total_steps: template?.default_steps.length || 6,
      progress_percentage: 0,
      files_created: [],
      errors: [],
      project_id: request.project_id,
      assigned_agents: request.assigned_agents || [],
      created_by: 'user_001', // TODO: Get from auth service
      tags: request.tags || [],
      priority: request.priority || WorkflowPriority.MEDIUM,
      metrics: {
        total_duration: 0,
        agent_time: {},
        files_generated: 0,
        lines_of_code: 0,
        tests_created: 0,
        cost_estimate: 0,
        success_rate: 0
      },
      steps: [],
      artifacts: []
    };

    this.workflows.update(workflows => [...workflows, newWorkflow]);
    return newWorkflow;
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
    this.workflows.update(workflows => workflows.filter(w => w.workflow_id !== workflowId));
  }

  /**
   * Cancel workflow
   */
  cancelWorkflow(workflowId: string): void {
    this.updateWorkflow(workflowId, {
      status: WorkflowStatus.CANCELLED,
      completed_at: new Date().toISOString()
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
}
