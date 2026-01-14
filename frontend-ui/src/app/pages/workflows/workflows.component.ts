import { Component, OnInit, OnDestroy, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialog } from '@angular/material/dialog';
import { WorkflowService } from '../../shared/services/workflow.service';
import {
  Workflow,
  WorkflowStatus,
  WorkflowType,
  WorkflowPriority
} from '../../core/interfaces/workflow.interface';
import { WorkflowCreateDialogComponent } from './workflow-create-dialog/workflow-create-dialog.component';

@Component({
  selector: 'app-workflows',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTooltipModule,
    MatTabsModule
  ],
  templateUrl: './workflows.component.html',
  styleUrl: './workflows.component.scss'
})
export class WorkflowsComponent implements OnInit, OnDestroy {
  private readonly workflowService = inject(WorkflowService);
  private readonly dialog = inject(MatDialog);

  // All workflows from service
  allWorkflows = this.workflowService.workflowsSignal;
  loading = this.workflowService.loadingSignal;

  // Statistics from service
  totalWorkflows = this.workflowService.totalWorkflows;
  runningCount = this.workflowService.runningCount;
  completedCount = this.workflowService.completedCount;
  failedCount = this.workflowService.failedCount;

  // Filter state
  searchTerm = signal<string>('');
  selectedStatus = signal<WorkflowStatus | 'all'>('all');
  selectedType = signal<WorkflowType | 'all'>('all');
  selectedPriority = signal<WorkflowPriority | 'all'>('all');
  selectedTab = signal<number>(0);

  // Enums for templates
  readonly WorkflowStatus = WorkflowStatus;
  readonly WorkflowType = WorkflowType;
  readonly WorkflowPriority = WorkflowPriority;

  // Filtered workflows based on current tab and filters
  filteredWorkflows = computed(() => {
    let workflows = this.allWorkflows();

    // Filter by tab (status)
    const tab = this.selectedTab();
    if (tab === 1) {
      workflows = workflows.filter(w => w.status === WorkflowStatus.RUNNING);
    } else if (tab === 2) {
      workflows = workflows.filter(w => w.status === WorkflowStatus.COMPLETED);
    } else if (tab === 3) {
      workflows = workflows.filter(w => w.status === WorkflowStatus.FAILED || w.status === WorkflowStatus.CANCELLED);
    }

    // Apply search filter
    const search = this.searchTerm().toLowerCase();
    if (search) {
      workflows = workflows.filter(w =>
        w.name.toLowerCase().includes(search) ||
        w.description.toLowerCase().includes(search) ||
        w.requirement.toLowerCase().includes(search) ||
        w.workflow_id.toLowerCase().includes(search)
      );
    }

    // Apply type filter
    const type = this.selectedType();
    if (type !== 'all') {
      workflows = workflows.filter(w => w.workflow_type === type);
    }

    // Apply priority filter
    const priority = this.selectedPriority();
    if (priority !== 'all') {
      workflows = workflows.filter(w => w.priority === priority);
    }

    // Sort by started_at (most recent first)
    return workflows.sort((a, b) =>
      new Date(b.started_at).getTime() - new Date(a.started_at).getTime()
    );
  });

  ngOnInit(): void {
    this.workflowService.loadWorkflows();
    // Enable auto-refresh for running workflows (every 5 seconds)
    this.workflowService.enableAutoRefresh(5000);
  }

  ngOnDestroy(): void {
    this.workflowService.disableAutoRefresh();
  }

  onTabChange(index: number): void {
    this.selectedTab.set(index);
  }

  refreshWorkflows(): void {
    this.workflowService.loadWorkflows();
  }

  cancelWorkflow(workflowId: string, event: Event): void {
    event.stopPropagation();
    if (confirm('Are you sure you want to cancel this workflow?')) {
      this.workflowService.cancelWorkflow(workflowId);
    }
  }

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

  getDuration(workflow: Workflow): string {
    if (workflow.duration) {
      const hours = Math.floor(workflow.duration / 3600);
      const minutes = Math.floor((workflow.duration % 3600) / 60);
      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      }
      return `${minutes}m`;
    }
    return 'N/A';
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

  clearFilters(): void {
    this.searchTerm.set('');
    this.selectedType.set('all');
    this.selectedPriority.set('all');
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(WorkflowCreateDialogComponent, {
      width: '900px',
      maxHeight: '90vh'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.workflowService.createWorkflow(result).subscribe(newWorkflow => {
          if (newWorkflow) {
            console.log('Workflow created:', newWorkflow);
          }
        });
      }
    });
  }
}
