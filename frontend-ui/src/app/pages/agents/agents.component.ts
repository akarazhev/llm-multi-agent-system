import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AgentService } from '../../shared/services/agent.service';
import { Agent, AgentRole } from '../../core/interfaces/agent.interface';

@Component({
  selector: 'app-agents',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatChipsModule,
    MatButtonModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './agents.component.html',
  styleUrl: './agents.component.scss'
})
export class AgentsComponent implements OnInit {
  private readonly agentService = inject(AgentService);

  agents = signal<Agent[]>([]);
  loading = signal(true);

  agentRoleDescriptions: Record<AgentRole, string> = {
    [AgentRole.BUSINESS_ANALYST]: 'Analyzes requirements and creates user stories',
    [AgentRole.DEVELOPER]: 'Designs architecture and implements features',
    [AgentRole.QA_ENGINEER]: 'Creates test suites and ensures quality',
    [AgentRole.DEVOPS_ENGINEER]: 'Sets up infrastructure and deployment pipelines',
    [AgentRole.TECHNICAL_WRITER]: 'Creates comprehensive documentation'
  };

  ngOnInit(): void {
    this.loadAgents();
  }

  private loadAgents(): void {
    this.loading.set(true);

    this.agentService.getAgents().subscribe({
      next: (agents) => {
        this.agents.set(agents);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading agents:', error);
        this.loading.set(false);
      }
    });
  }

  getAgentIcon(role: AgentRole): string {
    const icons: Record<AgentRole, string> = {
      [AgentRole.BUSINESS_ANALYST]: 'analytics',
      [AgentRole.DEVELOPER]: 'code',
      [AgentRole.QA_ENGINEER]: 'bug_report',
      [AgentRole.DEVOPS_ENGINEER]: 'cloud',
      [AgentRole.TECHNICAL_WRITER]: 'description'
    };
    return icons[role];
  }

  getStatusClass(status: string): string {
    return `status-${status.toLowerCase()}`;
  }

  refreshAgents(): void {
    this.loadAgents();
  }
}
