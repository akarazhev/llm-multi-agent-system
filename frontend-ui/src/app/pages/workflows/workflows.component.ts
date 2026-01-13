import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { WorkflowService } from '../../shared/services/workflow.service';
import { Workflow } from '../../core/interfaces/workflow.interface';

@Component({
  selector: 'app-workflows',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatDialogModule
  ],
  templateUrl: './workflows.component.html',
  styleUrl: './workflows.component.scss'
})
export class WorkflowsComponent implements OnInit {
  private readonly workflowService = inject(WorkflowService);
  private readonly dialog = inject(MatDialog);

  workflows = signal<Workflow[]>([]);
  loading = signal(true);

  displayedColumns = ['workflow_id', 'type', 'status', 'started_at', 'steps', 'actions'];

  ngOnInit(): void {
    this.loadWorkflows();
  }

  private loadWorkflows(): void {
    this.loading.set(true);
    
    this.workflowService.getWorkflows().subscribe({
      next: (workflows) => {
        this.workflows.set(workflows);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading workflows:', error);
        this.loading.set(false);
      }
    });
  }

  getStatusClass(status: string): string {
    return `status-${status.toLowerCase()}`;
  }

  refreshWorkflows(): void {
    this.loadWorkflows();
  }

  cancelWorkflow(workflowId: string): void {
    if (confirm('Are you sure you want to cancel this workflow?')) {
      this.workflowService.cancelWorkflow(workflowId).subscribe({
        next: () => {
          this.loadWorkflows();
        },
        error: (error) => {
          console.error('Error cancelling workflow:', error);
        }
      });
    }
  }

  resumeWorkflow(workflowId: string): void {
    this.workflowService.resumeWorkflow(workflowId).subscribe({
      next: () => {
        this.loadWorkflows();
      },
      error: (error) => {
        console.error('Error resuming workflow:', error);
      }
    });
  }

  getWorkflowIcon(type: string): string {
    const icons: Record<string, string> = {
      'feature_development': 'build',
      'bug_fix': 'bug_report',
      'infrastructure': 'cloud',
      'documentation': 'description',
      'analysis': 'analytics'
    };
    return icons[type] || 'account_tree';
  }
}
