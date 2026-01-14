import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, finalize, of, tap } from 'rxjs';
import { Agent, AgentTemplate, CreateAgentRequest, AgentRole, AgentStatus } from '../../core/interfaces/agent.interface';
import { AGENT_TEMPLATES } from '../../mocks/mock-agents';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;
  private agents = signal<Agent[]>([]);
  private templates = signal<AgentTemplate[]>([...AGENT_TEMPLATES]);
  private loading = signal<boolean>(false);

  // Public read-only signals
  readonly agentsSignal = this.agents.asReadonly();
  readonly templatesSignal = this.templates.asReadonly();
  readonly loadingSignal = this.loading.asReadonly();

  // Computed signals
  readonly activeAgents = computed(() => 
    this.agents().filter(a => a.status === AgentStatus.WORKING || a.status === AgentStatus.IDLE)
  );

  readonly agentsByRole = computed(() => {
    const byRole = new Map<AgentRole, Agent[]>();
    this.agents().forEach(agent => {
      const existing = byRole.get(agent.role) || [];
      byRole.set(agent.role, [...existing, agent]);
    });
    return byRole;
  });

  readonly totalAgents = computed(() => this.agents().length);
  readonly activeAgentsCount = computed(() => this.activeAgents().length);

  constructor() {
    // Simulate loading agents on service init
    this.loadAgents();
  }

  /**
   * Load all agents from backend (simulated with mock data)
   */
  loadAgents(): void {
    this.loading.set(true);
    this.http.get<Agent[]>(`${this.apiUrl}/agents`).pipe(
      catchError(() => of([])),
      finalize(() => this.loading.set(false))
    ).subscribe(agents => this.agents.set(agents));
  }

  /**
   * Get agent by ID
   */
  getAgentById(id: string) {
    return this.http.get<Agent>(`${this.apiUrl}/agents/${id}`).pipe(
      catchError(() => of(undefined))
    );
  }

  /**
   * Get agents by project ID
   */
  getAgentsByProject(projectId: string): Agent[] {
    return this.agents().filter(a => a.assigned_projects?.includes(projectId));
  }

  /**
   * Get template by ID
   */
  getTemplateById(id: string): AgentTemplate | undefined {
    return this.templates().find(t => t.template_id === id);
  }

  /**
   * Create a new agent
   */
  createAgent(request: CreateAgentRequest) {
    return this.http.post<Agent>(`${this.apiUrl}/agents`, request).pipe(
      tap(agent => this.agents.update(agents => [...agents, agent])),
      catchError(() => of(undefined))
    );
  }

  /**
   * Update agent configuration
   */
  updateAgent(agentId: string, updates: Partial<Agent>): void {
    this.agents.update(agents => 
      agents.map(a => a.agent_id === agentId ? { ...a, ...updates } : a)
    );
  }

  /**
   * Delete agent
   */
  deleteAgent(agentId: string): void {
    this.http.delete(`${this.apiUrl}/agents/${agentId}`).pipe(
      catchError(() => of(null))
    ).subscribe(() => {
      this.agents.update(agents => agents.filter(a => a.agent_id !== agentId));
    });
  }

  /**
   * Assign agent to project
   */
  assignToProject(agentId: string, projectId: string): void {
    this.agents.update(agents => 
      agents.map(a => {
        if (a.agent_id === agentId) {
          const projects = a.assigned_projects || [];
          if (!projects.includes(projectId)) {
            return { ...a, assigned_projects: [...projects, projectId] };
          }
        }
        return a;
      })
    );
  }

  /**
   * Unassign agent from project
   */
  unassignFromProject(agentId: string, projectId: string): void {
    this.agents.update(agents => 
      agents.map(a => {
        if (a.agent_id === agentId) {
          const projects = a.assigned_projects || [];
          return { ...a, assigned_projects: projects.filter(p => p !== projectId) };
        }
        return a;
      })
    );
  }

  /**
   * Get role display name
   */
  getRoleDisplayName(role: AgentRole): string {
    const names: Record<AgentRole, string> = {
      [AgentRole.BUSINESS_ANALYST]: 'Business Analyst',
      [AgentRole.DEVELOPER]: 'Developer',
      [AgentRole.QA_ENGINEER]: 'QA Engineer',
      [AgentRole.DEVOPS_ENGINEER]: 'DevOps Engineer',
      [AgentRole.TECHNICAL_WRITER]: 'Technical Writer',
      [AgentRole.ARCHITECT]: 'Architect',
      [AgentRole.PRODUCT_MANAGER]: 'Product Manager',
      [AgentRole.SECURITY_ENGINEER]: 'Security Engineer'
    };
    return names[role] || role;
  }

  /**
   * Get role icon
   */
  getRoleIcon(role: AgentRole): string {
    const icons: Record<AgentRole, string> = {
      [AgentRole.BUSINESS_ANALYST]: 'analytics',
      [AgentRole.DEVELOPER]: 'code',
      [AgentRole.QA_ENGINEER]: 'bug_report',
      [AgentRole.DEVOPS_ENGINEER]: 'settings',
      [AgentRole.TECHNICAL_WRITER]: 'description',
      [AgentRole.ARCHITECT]: 'architecture',
      [AgentRole.PRODUCT_MANAGER]: 'business_center',
      [AgentRole.SECURITY_ENGINEER]: 'security'
    };
    return icons[role] || 'smart_toy';
  }
}
