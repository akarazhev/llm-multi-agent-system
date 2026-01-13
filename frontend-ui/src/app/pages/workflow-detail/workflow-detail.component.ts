import { Component, OnInit, OnDestroy, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { WorkflowService } from '../../shared/services/workflow.service';
import { AgentService } from '../../shared/services/agent.service';
import { ProjectService } from '../../shared/services/project.service';
import {
  Workflow,
  WorkflowStatus,
  WorkflowType,
  WorkflowPriority,
  StepStatus
} from '../../core/interfaces/workflow.interface';

@Component({
  selector: 'app-workflow-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatExpansionModule,
    MatTabsModule,
    MatTooltipModule,
    MatDividerModule,
    MatListModule
  ],
  templateUrl: './workflow-detail.component.html',
  styleUrl: './workflow-detail.component.scss'
})
export class WorkflowDetailComponent implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly workflowService = inject(WorkflowService);
  private readonly agentService = inject(AgentService);
  private readonly projectService = inject(ProjectService);

  workflow = signal<Workflow | undefined>(undefined);
  loading = signal(true);

  workflowExists = computed(() => !!this.workflow());

  // Get assigned agents for this workflow
  assignedAgents = computed(() => {
    const w = this.workflow();
    if (!w || !w.assigned_agents || w.assigned_agents.length === 0) return [];
    return this.agentService.agentsSignal().filter(agent =>
      w.assigned_agents.includes(agent.agent_id)
    );
  });

  // Get assigned project (synchronous)
  assignedProject = computed(() => {
    const w = this.workflow();
    if (!w || !w.project_id) return undefined;
    // getProjectById returns Project | undefined, not Observable
    const projects = this.projectService.projects();
    return projects.find(p => p.id === w.project_id);
  });

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const workflowId = params.get('id');
      if (workflowId) {
        this.loadWorkflow(workflowId);
      }
    });
    // Enable auto-refresh for this workflow if it's running
    this.workflowService.enableAutoRefresh(5000);
  }

  ngOnDestroy(): void {
    this.workflowService.disableAutoRefresh();
  }

  private loadWorkflow(id: string): void {
    this.loading.set(true);
    const workflow = this.workflowService.getWorkflowById(id);
    if (workflow) {
      this.workflow.set(workflow);
    } else {
      this.workflow.set(undefined);
    }
    this.loading.set(false);
  }

  goBack(): void {
    this.router.navigate(['/workflows']);
  }

  refreshWorkflow(): void {
    const workflowId = this.route.snapshot.paramMap.get('id');
    if (workflowId) {
      this.workflowService.loadWorkflows();
      this.loadWorkflow(workflowId);
    }
  }

  cancelWorkflow(): void {
    const workflowId = this.workflow()?.workflow_id;
    if (!workflowId) return;

    if (confirm('Are you sure you want to cancel this workflow?')) {
      this.workflowService.cancelWorkflow(workflowId);
      this.loadWorkflow(workflowId);
    }
  }

  deleteWorkflow(): void {
    const workflow = this.workflow();
    if (!workflow) return;

    if (confirm(`Are you sure you want to delete workflow "${workflow.name}"?`)) {
      this.workflowService.deleteWorkflow(workflow.workflow_id);
      this.router.navigate(['/workflows']);
    }
  }

  // UI Helpers
  getStatusClass(status: WorkflowStatus): string {
    return `status-${status.toLowerCase()}`;
  }

  getStatusIcon(status: WorkflowStatus): string {
    switch (status) {
      case WorkflowStatus.PENDING:
        return 'schedule';
      case WorkflowStatus.RUNNING:
        return 'play_circle_outline';
      case WorkflowStatus.PAUSED:
        return 'pause_circle_outline';
      case WorkflowStatus.COMPLETED:
        return 'check_circle_outline';
      case WorkflowStatus.FAILED:
        return 'error_outline';
      case WorkflowStatus.CANCELLED:
        return 'cancel';
      default:
        return 'info';
    }
  }

  getStepStatusClass(status: StepStatus): string {
    return `step-status-${status.toLowerCase().replace('_', '-')}`;
  }

  getStepStatusIcon(status: StepStatus): string {
    switch (status) {
      case StepStatus.PENDING:
        return 'radio_button_unchecked';
      case StepStatus.IN_PROGRESS:
        return 'radio_button_checked';
      case StepStatus.COMPLETED:
        return 'check_circle';
      case StepStatus.FAILED:
        return 'error';
      case StepStatus.SKIPPED:
        return 'remove_circle';
      default:
        return 'help';
    }
  }

  getTypeIcon(type: WorkflowType): string {
    return this.workflowService.getTypeIcon(type);
  }

  getTypeDisplayName(type: WorkflowType): string {
    return this.workflowService.getTypeDisplayName(type);
  }

  getPriorityIcon(priority: WorkflowPriority): string {
    switch (priority) {
      case WorkflowPriority.CRITICAL:
        return 'priority_high';
      case WorkflowPriority.HIGH:
        return 'arrow_upward';
      case WorkflowPriority.MEDIUM:
        return 'drag_handle';
      case WorkflowPriority.LOW:
        return 'arrow_downward';
      default:
        return 'drag_handle';
    }
  }

  getPriorityClass(priority: WorkflowPriority): string {
    return `priority-${priority.toLowerCase()}`;
  }

  getDuration(seconds?: number): string {
    if (!seconds) return 'N/A';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    }
    return `${secs}s`;
  }

  getTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString();
  }

  getArtifactIcon(type: string): string {
    switch (type) {
      case 'code':
        return 'code';
      case 'documentation':
        return 'description';
      case 'test':
        return 'science';
      case 'config':
        return 'settings';
      case 'diagram':
        return 'account_tree';
      default:
        return 'insert_drive_file';
    }
  }

  formatBytes(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  // Expose Object for template use
  readonly Object = Object;
}
