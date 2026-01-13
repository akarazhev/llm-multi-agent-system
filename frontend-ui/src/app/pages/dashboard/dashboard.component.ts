import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { RouterModule } from '@angular/router';
import { AgentService } from '../../shared/services/agent.service';
import { WorkflowService } from '../../shared/services/workflow.service';
import { Agent } from '../../core/interfaces/agent.interface';
import { Workflow } from '../../core/interfaces/workflow.interface';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatChipsModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  private readonly agentService = inject(AgentService);
  private readonly workflowService = inject(WorkflowService);

  agents = signal<Agent[]>([]);
  recentWorkflows = signal<Workflow[]>([]);
  loading = signal(true);

  stats = signal({
    totalAgents: 5,
    activeWorkflows: 0,
    completedToday: 0,
    totalWorkflows: 0
  });

  ngOnInit(): void {
    this.loadDashboardData();
  }

  private loadDashboardData(): void {
    this.loading.set(true);

    // Load agents
    this.agentService.getAgents().subscribe({
      next: (agents) => {
        this.agents.set(agents);
      },
      error: (error) => {
        console.error('Error loading agents:', error);
      }
    });

    // Load recent workflows
    this.workflowService.getWorkflows().subscribe({
      next: (workflows) => {
        this.recentWorkflows.set(workflows.slice(0, 5)); // Last 5 workflows
        
        // Calculate stats
        const activeWorkflows = workflows.filter(w => w.status === 'running').length;
        const today = new Date().toDateString();
        const completedToday = workflows.filter(w => 
          w.completed_at && new Date(w.completed_at).toDateString() === today
        ).length;

        this.stats.set({
          totalAgents: 5,
          activeWorkflows,
          completedToday,
          totalWorkflows: workflows.length
        });

        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading workflows:', error);
        this.loading.set(false);
      }
    });
  }

  getAgentStatusClass(status: string): string {
    return `status-${status.toLowerCase()}`;
  }

  getWorkflowStatusClass(status: string): string {
    return `workflow-status-${status.toLowerCase()}`;
  }

  refreshDashboard(): void {
    this.loadDashboardData();
  }
}
