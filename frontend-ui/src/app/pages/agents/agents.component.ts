import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AgentService } from '../../shared/services/agent.service';
import { Agent, AgentTemplate, AgentRole, AgentStatus, CreateAgentRequest } from '../../core/interfaces/agent.interface';
import { AgentConfigDialogComponent } from './agent-config-dialog/agent-config-dialog.component';

@Component({
  selector: 'app-agents',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatIconModule,
    MatChipsModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatTabsModule,
    MatBadgeModule,
    MatTooltipModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './agents.component.html',
  styleUrl: './agents.component.scss'
})
export class AgentsComponent {
  readonly agentService = inject(AgentService);
  private readonly dialog = inject(MatDialog);
  private readonly snackBar = inject(MatSnackBar);

  // Signals from service
  readonly agents = this.agentService.agentsSignal;
  readonly templates = this.agentService.templatesSignal;
  readonly loading = this.agentService.loadingSignal;

  // Local signals
  readonly selectedTab = signal(0);
  readonly searchQuery = signal('');

  // Computed signals
  readonly filteredAgents = computed(() => {
    const query = this.searchQuery().toLowerCase();
    if (!query) return this.agents();
    return this.agents().filter(a => 
      a.name.toLowerCase().includes(query) || 
      a.role.toLowerCase().includes(query) ||
      a.description.toLowerCase().includes(query)
    );
  });

  readonly agentsByStatus = computed(() => {
    const byStatus = {
      working: [] as Agent[],
      idle: [] as Agent[],
      offline: [] as Agent[],
      error: [] as Agent[]
    };
    this.agents().forEach(agent => {
      if (agent.status === AgentStatus.WORKING) byStatus.working.push(agent);
      else if (agent.status === AgentStatus.IDLE) byStatus.idle.push(agent);
      else if (agent.status === AgentStatus.OFFLINE) byStatus.offline.push(agent);
      else if (agent.status === AgentStatus.ERROR) byStatus.error.push(agent);
    });
    return byStatus;
  });

  readonly stats = computed(() => ({
    total: this.agents().length,
    working: this.agentsByStatus().working.length,
    idle: this.agentsByStatus().idle.length,
    offline: this.agentsByStatus().offline.length,
    error: this.agentsByStatus().error.length
  }));

  refreshAgents(): void {
    this.agentService.loadAgents();
  }

  createAgentFromTemplate(template: AgentTemplate): void {
    const dialogRef = this.dialog.open(AgentConfigDialogComponent, {
      width: '700px',
      maxWidth: '90vw',
      data: {
        template,
        mode: 'create'
      },
      disableClose: false
    });

    dialogRef.afterClosed().subscribe((request: CreateAgentRequest) => {
      if (request) {
        this.agentService.createAgent(request).subscribe(newAgent => {
          if (newAgent) {
            this.snackBar.open(`Agent "${newAgent.name}" created successfully!`, 'Close', {
              duration: 3000,
              horizontalPosition: 'end',
              verticalPosition: 'top'
            });
            // Switch to Active Agents tab
            this.selectedTab.set(0);
          }
        });
      }
    });
  }

  viewAgentDetails(agent: Agent): void {
    this.router.navigate(['/agents', agent.agent_id]);
  }

  private router = inject(Router);

  getStatusClass(status: AgentStatus): string {
    return `status-${status.toLowerCase()}`;
  }

  getStatusIcon(status: AgentStatus): string {
    const icons: Record<AgentStatus, string> = {
      [AgentStatus.IDLE]: 'pause_circle',
      [AgentStatus.WORKING]: 'play_circle',
      [AgentStatus.WAITING]: 'schedule',
      [AgentStatus.COMPLETED]: 'check_circle',
      [AgentStatus.ERROR]: 'error',
      [AgentStatus.OFFLINE]: 'offline_bolt'
    };
    return icons[status] || 'help';
  }

  getRoleDisplayName(role: AgentRole): string {
    return this.agentService.getRoleDisplayName(role);
  }

  getRoleIcon(role: AgentRole): string {
    return this.agentService.getRoleIcon(role);
  }

  formatCost(cost: number): string {
    return `$${cost.toFixed(2)}`;
  }

  formatNumber(num: number): string {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  }
}
