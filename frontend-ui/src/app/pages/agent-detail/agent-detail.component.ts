import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDividerModule } from '@angular/material/divider';
import { AgentService } from '../../shared/services/agent.service';
import { Agent, AgentStatus } from '../../core/interfaces/agent.interface';

@Component({
  selector: 'app-agent-detail',
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
    MatTooltipModule,
    MatDividerModule
  ],
  templateUrl: './agent-detail.component.html',
  styleUrl: './agent-detail.component.scss'
})
export class AgentDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly agentService = inject(AgentService);

  readonly agent = signal<Agent | undefined>(undefined);
  readonly loading = signal(true);
  readonly agentExists = computed(() => !!this.agent());

  ngOnInit(): void {
    const agentId = this.route.snapshot.paramMap.get('id');
    if (agentId) {
      this.loadAgent(agentId);
    } else {
      this.loading.set(false);
    }
  }

  private loadAgent(id: string): void {
    this.loading.set(true);
    // Simulate API call
    setTimeout(() => {
      const foundAgent = this.agentService.getAgentById(id);
      this.agent.set(foundAgent);
      this.loading.set(false);
    }, 500);
  }

  goBack(): void {
    this.router.navigate(['/agents']);
  }

  editAgent(): void {
    // TODO: Open edit dialog
    console.log('Edit agent:', this.agent());
  }

  deleteAgent(): void {
    if (confirm(`Are you sure you want to delete ${this.agent()?.name}?`)) {
      this.agentService.deleteAgent(this.agent()!.agent_id);
      this.router.navigate(['/agents']);
    }
  }

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

  getRoleIcon(): string {
    return this.agent() ? this.agentService.getRoleIcon(this.agent()!.role) : 'smart_toy';
  }

  getRoleDisplayName(): string {
    return this.agent() ? this.agentService.getRoleDisplayName(this.agent()!.role) : '';
  }

  formatCost(cost: number): string {
    return `$${cost.toFixed(2)}`;
  }

  formatNumber(num: number): string {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  }

  getTimeAgo(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor(diff / (1000 * 60));

    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return 'just now';
  }
}
