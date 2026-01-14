import { Component, OnInit, OnDestroy, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
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
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { WorkflowService } from '../../shared/services/workflow.service';
import { AgentService } from '../../shared/services/agent.service';
import { ProjectService } from '../../shared/services/project.service';
import { CommunicationService } from '../../shared/services/communication.service';
import { WebSocketService, WorkflowWsMessage } from '../../shared/services/websocket.service';
import {
  Workflow,
  WorkflowStatus,
  WorkflowType,
  WorkflowPriority,
  StepStatus
} from '../../core/interfaces/workflow.interface';
import {
  AgentMessage,
  MessageType,
  MessageThread,
  CommunicationStats
} from '../../core/interfaces/agent-message.interface';
import { AgentRole } from '../../core/interfaces/agent.interface';

@Component({
  selector: 'app-workflow-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
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
    MatListModule,
    MatButtonToggleModule,
    MatFormFieldModule,
    MatSelectModule
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
  private readonly communicationService = inject(CommunicationService);
  private readonly websocketService = inject(WebSocketService);

  workflow = signal<Workflow | undefined>(undefined);
  loading = signal(true);
  messagesSignal = signal<AgentMessage[]>([]);
  threadsSignal = signal<MessageThread[]>([]);
  communicationStatsSignal = signal<CommunicationStats | null>(null);
  private wsSubscription?: Subscription;
  private routeSubscription?: Subscription;

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
    this.routeSubscription = this.route.paramMap.subscribe(params => {
      const workflowId = params.get('id');
      if (workflowId) {
        this.loadWorkflow(workflowId);
        this.loadCommunication(workflowId);
        this.websocketService.connect(workflowId);
        this.wsSubscription?.unsubscribe();
        this.wsSubscription = this.websocketService.messages$.subscribe(message => {
          this.handleWsMessage(message);
        });
      }
    });
    // Enable auto-refresh for this workflow if it's running
    this.workflowService.enableAutoRefresh(5000);
  }

  ngOnDestroy(): void {
    this.workflowService.disableAutoRefresh();
    this.websocketService.disconnect();
    this.wsSubscription?.unsubscribe();
    this.routeSubscription?.unsubscribe();
  }

  private loadWorkflow(id: string): void {
    this.loading.set(true);
    this.workflowService.getWorkflowById(id).subscribe(workflow => {
      this.workflow.set(workflow);
      this.loading.set(false);
    });
  }

  private loadCommunication(workflowId: string): void {
    this.communicationService.getMessages(workflowId).subscribe(messages => {
      this.messagesSignal.set(messages);
    });
    this.communicationService.getThreads(workflowId).subscribe(threads => {
      this.threadsSignal.set(threads);
    });
    this.communicationService.getStats(workflowId).subscribe(stats => {
      this.communicationStatsSignal.set(stats);
    });
  }

  private handleWsMessage(message: WorkflowWsMessage): void {
    if (message.event_type === 'workflow_status_changed') {
      const workflowId = this.workflow()?.workflow_id;
      if (workflowId) {
        this.loadWorkflow(workflowId);
      }
    }
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

  // ==================== Communication Features ====================

  // Communication data
  messages = computed(() => {
    return this.messagesSignal();
  });

  messageThreads = computed(() => {
    return this.threadsSignal();
  });

  communicationStats = computed(() => {
    const stats = this.communicationStatsSignal();
    return stats ?? {
      total_messages: 0,
      messages_by_type: {},
      messages_by_agent: {},
      threads_count: 0,
      open_threads: 0,
      resolved_threads: 0,
      decisions_count: 0,
      average_response_time_seconds: 0
    };
  });

  // Communication filters
  messageTypeFilter = signal<string>('all');
  agentFilter = signal<string>('all');
  viewMode = signal<'chat' | 'threads'>('chat');

  // Filtered messages
  filteredMessages = computed(() => {
    let msgs = this.messages();
    
    const typeFilter = this.messageTypeFilter();
    if (typeFilter !== 'all') {
      msgs = msgs.filter(m => m.message_type === typeFilter);
    }
    
    const agentFilterValue = this.agentFilter();
    if (agentFilterValue !== 'all') {
      msgs = msgs.filter(m => m.agent_id === agentFilterValue);
    }
    
    return msgs;
  });

  // Communication helper methods
  getAgentIcon(role: AgentRole): string {
    switch (role) {
      case AgentRole.BUSINESS_ANALYST: return 'analytics';
      case AgentRole.DEVELOPER: return 'code';
      case AgentRole.QA_ENGINEER: return 'bug_report';
      case AgentRole.DEVOPS_ENGINEER: return 'cloud';
      case AgentRole.TECHNICAL_WRITER: return 'description';
      case AgentRole.ARCHITECT: return 'architecture';
      case AgentRole.PRODUCT_MANAGER: return 'leaderboard';
      case AgentRole.SECURITY_ENGINEER: return 'security';
      default: return 'smart_toy';
    }
  }

  getMessageTypeIcon(type: MessageType): string {
    switch (type) {
      case MessageType.QUESTION: return 'help';
      case MessageType.PROPOSAL: return 'lightbulb';
      case MessageType.ANSWER: return 'chat';
      case MessageType.DECISION: return 'gavel';
      case MessageType.CLARIFICATION: return 'info';
      case MessageType.SYNCHRONIZATION: return 'sync';
      case MessageType.ERROR_REPORT: return 'error';
      case MessageType.COMPLETION: return 'check_circle';
      default: return 'message';
    }
  }

  getAttachmentIcon(type: string): string {
    switch (type) {
      case 'code': return 'code';
      case 'file': return 'insert_drive_file';
      case 'link': return 'link';
      case 'image': return 'image';
      default: return 'attach_file';
    }
  }

  formatMessageContent(content: string): string {
    // Simple formatting: convert newlines to <br>, preserve code blocks
    return content
      .replace(/\n/g, '<br>')
      .replace(/`([^`]+)`/g, '<code>$1</code>');
  }

  formatSeconds(seconds: number): string {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    return `${hours}h ${minutes % 60}m`;
  }

  // Expose Object for template use
  readonly Object = Object;
}
