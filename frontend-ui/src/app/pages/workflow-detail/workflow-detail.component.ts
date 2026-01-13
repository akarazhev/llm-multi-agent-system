import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatExpansionModule } from '@angular/material/expansion';
import { WorkflowService } from '../../shared/services/workflow.service';
import { WorkflowState } from '../../core/interfaces/workflow.interface';

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
    MatExpansionModule
  ],
  templateUrl: './workflow-detail.component.html',
  styleUrl: './workflow-detail.component.scss'
})
export class WorkflowDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly workflowService = inject(WorkflowService);

  workflow = signal<WorkflowState | null>(null);
  loading = signal(true);

  ngOnInit(): void {
    const workflowId = this.route.snapshot.paramMap.get('id');
    if (workflowId) {
      this.loadWorkflowDetails(workflowId);
    }
  }

  private loadWorkflowDetails(workflowId: string): void {
    this.loading.set(true);

    this.workflowService.getWorkflow(workflowId).subscribe({
      next: (workflow) => {
        this.workflow.set(workflow);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading workflow:', error);
        this.loading.set(false);
      }
    });
  }

  getStatusClass(status: string): string {
    return `status-${status.toLowerCase()}`;
  }

  getProgressPercentage(): number {
    const workflow = this.workflow();
    if (!workflow) return 0;
    
    // Total expected steps for a feature development workflow
    const totalSteps = 6;
    return (workflow.completed_steps.length / totalSteps) * 100;
  }

  refreshWorkflow(): void {
    const workflowId = this.route.snapshot.paramMap.get('id');
    if (workflowId) {
      this.loadWorkflowDetails(workflowId);
    }
  }
}
