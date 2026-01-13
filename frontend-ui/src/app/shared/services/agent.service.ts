import { Injectable, signal, computed } from '@angular/core';
import { Agent, AgentTemplate, CreateAgentRequest, AgentRole, AgentStatus } from '../../core/interfaces/agent.interface';
import { MOCK_AGENTS, AGENT_TEMPLATES } from '../../mocks/mock-agents';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private agents = signal<Agent[]>([...MOCK_AGENTS]);
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
    // Simulate API call
    setTimeout(() => {
      this.agents.set([...MOCK_AGENTS]);
      this.loading.set(false);
    }, 500);
  }

  /**
   * Get agent by ID
   */
  getAgentById(id: string): Agent | undefined {
    return this.agents().find(a => a.agent_id === id);
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
  createAgent(request: CreateAgentRequest): Agent {
    const template = request.template_id 
      ? this.getTemplateById(request.template_id)
      : undefined;

    const newAgent: Agent = {
      agent_id: `agent_${Date.now()}`,
      name: request.name,
      role: request.role,
      status: AgentStatus.IDLE,
      description: request.description || '',
      capabilities: template?.capabilities || [],
      completed_tasks: 0,
      failed_tasks: 0,
      created_at: new Date().toISOString(),
      configuration: {
        ...(template?.default_configuration || {
          model: 'llama3-70b',
          temperature: 0.5,
          max_tokens: 4000,
          tools_enabled: [],
          auto_approve: false,
          max_retries: 3
        }),
        ...(request.configuration || {})
      },
      metrics: {
        total_tasks: 0,
        success_rate: 0,
        avg_response_time: 0,
        tokens_used: 0,
        cost_estimate: 0
      },
      assigned_projects: []
    };

    this.agents.update(agents => [...agents, newAgent]);
    return newAgent;
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
    this.agents.update(agents => agents.filter(a => a.agent_id !== agentId));
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
