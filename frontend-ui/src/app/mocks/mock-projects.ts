import { Project } from '../core/interfaces/project.interface';

export const mockProjects: Project[] = [
  {
    id: 'proj-1',
    name: 'SPP Core UI',
    description: 'Santander Payment Platform core user interface application',
    icon: '📊',
    status: 'active',
    type: 'web_app',
    ownerId: 'user-1',
    teamMembers: [
      {
        userId: 'user-1',
        name: 'Alexey Mikhalchenkov',
        email: 'alexey.mikhalchenkov@specific-group.com',
        role: 'Project Lead',
        accessLevel: 'owner',
        joinedAt: '2024-01-15T10:00:00Z'
      },
      {
        userId: 'user-2',
        name: 'Maria Garcia',
        email: 'maria.garcia@specific-group.com',
        role: 'Frontend Developer',
        accessLevel: 'developer',
        joinedAt: '2024-01-20T10:00:00Z'
      },
      {
        userId: 'user-3',
        name: 'John Smith',
        email: 'john.smith@specific-group.com',
        role: 'Backend Developer',
        accessLevel: 'developer',
        joinedAt: '2024-02-01T10:00:00Z'
      }
    ],
    aiAgents: ['business_analyst', 'developer', 'qa_engineer', 'technical_writer'],
    integrations: {
      git: {
        platform: 'github',
        url: 'https://github.com/santander/spp-core-ui',
        branch: 'main',
        connected: true,
        lastSync: '2026-01-14T00:30:00Z'
      },
      jira: {
        url: 'https://santander.atlassian.net',
        projectKey: 'SPP',
        connected: true,
        lastSync: '2026-01-14T00:25:00Z'
      },
      confluence: {
        spaceKey: 'SPP-DOCS',
        connected: true,
        lastSync: '2026-01-13T22:00:00Z'
      },
      slack: {
        channel: '#spp-notifications',
        connected: true
      }
    },
    techStack: {
      languages: ['TypeScript', 'SCSS', 'HTML'],
      frameworks: ['Angular 20', 'Material Design', 'RxJS'],
      databases: ['PostgreSQL'],
      tools: ['ESLint', 'Prettier', 'Karma', 'Protractor']
    },
    stats: {
      totalWorkflows: 24,
      activeWorkflows: 3,
      completedWorkflows: 19,
      failedWorkflows: 2,
      teamSize: 3,
      aiAgentsCount: 4,
      filesGenerated: 156,
      linesOfCode: 45230
    },
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2026-01-14T00:30:00Z',
    lastActivity: '2026-01-14T00:30:00Z'
  },
  {
    id: 'proj-2',
    name: 'LLM Multi-Agent System',
    description: 'AI-powered development automation platform with multiple specialized agents',
    icon: '🤖',
    status: 'active',
    type: 'api',
    ownerId: 'user-1',
    teamMembers: [
      {
        userId: 'user-1',
        name: 'Alexey Mikhalchenkov',
        email: 'alexey.mikhalchenkov@specific-group.com',
        role: 'Lead Developer',
        accessLevel: 'owner',
        joinedAt: '2025-12-01T10:00:00Z'
      },
      {
        userId: 'user-4',
        name: 'Anna Kowalski',
        email: 'anna.kowalski@specific-group.com',
        role: 'ML Engineer',
        accessLevel: 'developer',
        joinedAt: '2025-12-10T10:00:00Z'
      }
    ],
    aiAgents: ['business_analyst', 'developer', 'qa_engineer', 'devops_engineer', 'technical_writer'],
    integrations: {
      git: {
        platform: 'github',
        url: 'https://github.com/cursor/llm-multi-agent-system',
        branch: 'sdlc2.0',
        connected: true,
        lastSync: '2026-01-14T00:42:00Z'
      }
    },
    techStack: {
      languages: ['Python', 'TypeScript'],
      frameworks: ['FastAPI', 'LangGraph', 'Angular 20'],
      databases: ['SQLite', 'ChromaDB'],
      tools: ['Docker', 'pytest', 'Black']
    },
    stats: {
      totalWorkflows: 8,
      activeWorkflows: 1,
      completedWorkflows: 6,
      failedWorkflows: 1,
      teamSize: 2,
      aiAgentsCount: 5,
      filesGenerated: 48,
      linesOfCode: 12450
    },
    createdAt: '2025-12-01T10:00:00Z',
    updatedAt: '2026-01-14T00:42:00Z',
    lastActivity: '2026-01-14T00:42:00Z'
  },
  {
    id: 'proj-3',
    name: 'Payment Gateway API',
    description: 'High-performance payment processing API with multi-currency support',
    icon: '💰',
    status: 'active',
    type: 'api',
    ownerId: 'user-5',
    teamMembers: [
      {
        userId: 'user-5',
        name: 'Carlos Rodriguez',
        email: 'carlos.rodriguez@specific-group.com',
        role: 'Backend Lead',
        accessLevel: 'owner',
        joinedAt: '2024-03-01T10:00:00Z'
      }
    ],
    aiAgents: ['developer', 'qa_engineer', 'devops_engineer'],
    integrations: {
      git: {
        platform: 'gitlab',
        url: 'https://gitlab.com/santander/payment-api',
        branch: 'main',
        connected: true,
        lastSync: '2026-01-13T20:00:00Z'
      },
      jira: {
        url: 'https://santander.atlassian.net',
        projectKey: 'PAY',
        connected: true,
        lastSync: '2026-01-13T19:00:00Z'
      }
    },
    techStack: {
      languages: ['Java', 'Kotlin'],
      frameworks: ['Spring Boot', 'Hibernate'],
      databases: ['PostgreSQL', 'Redis'],
      tools: ['Maven', 'JUnit', 'Mockito']
    },
    stats: {
      totalWorkflows: 15,
      activeWorkflows: 2,
      completedWorkflows: 12,
      failedWorkflows: 1,
      teamSize: 1,
      aiAgentsCount: 3,
      filesGenerated: 89,
      linesOfCode: 28600
    },
    createdAt: '2024-03-01T10:00:00Z',
    updatedAt: '2026-01-13T20:00:00Z',
    lastActivity: '2026-01-13T20:00:00Z'
  },
  {
    id: 'proj-4',
    name: 'Mobile Banking App',
    description: 'Cross-platform mobile application for retail banking',
    icon: '📱',
    status: 'planning',
    type: 'mobile_app',
    ownerId: 'user-6',
    teamMembers: [
      {
        userId: 'user-6',
        name: 'Sarah Johnson',
        email: 'sarah.johnson@specific-group.com',
        role: 'Mobile Lead',
        accessLevel: 'owner',
        joinedAt: '2026-01-05T10:00:00Z'
      }
    ],
    aiAgents: ['business_analyst', 'developer'],
    integrations: {},
    techStack: {
      languages: ['TypeScript', 'Dart'],
      frameworks: ['React Native', 'Flutter'],
      databases: [],
      tools: ['Expo', 'Jest']
    },
    stats: {
      totalWorkflows: 2,
      activeWorkflows: 0,
      completedWorkflows: 2,
      failedWorkflows: 0,
      teamSize: 1,
      aiAgentsCount: 2,
      filesGenerated: 12,
      linesOfCode: 3200
    },
    createdAt: '2026-01-05T10:00:00Z',
    updatedAt: '2026-01-10T15:00:00Z',
    lastActivity: '2026-01-10T15:00:00Z'
  },
  {
    id: 'proj-5',
    name: 'Infrastructure Automation',
    description: 'DevOps automation and infrastructure as code project',
    icon: '🔧',
    status: 'on_hold',
    type: 'infrastructure',
    ownerId: 'user-7',
    teamMembers: [
      {
        userId: 'user-7',
        name: 'Michael Chen',
        email: 'michael.chen@specific-group.com',
        role: 'DevOps Engineer',
        accessLevel: 'owner',
        joinedAt: '2024-06-01T10:00:00Z'
      }
    ],
    aiAgents: ['devops_engineer', 'technical_writer'],
    integrations: {
      git: {
        platform: 'github',
        url: 'https://github.com/santander/infra-automation',
        branch: 'main',
        connected: true,
        lastSync: '2025-12-20T10:00:00Z'
      }
    },
    techStack: {
      languages: ['Python', 'Bash', 'YAML'],
      frameworks: ['Terraform', 'Ansible'],
      databases: [],
      tools: ['Docker', 'Kubernetes', 'Helm']
    },
    stats: {
      totalWorkflows: 6,
      activeWorkflows: 0,
      completedWorkflows: 5,
      failedWorkflows: 1,
      teamSize: 1,
      aiAgentsCount: 2,
      filesGenerated: 34,
      linesOfCode: 8900
    },
    createdAt: '2024-06-01T10:00:00Z',
    updatedAt: '2025-12-20T10:00:00Z',
    lastActivity: '2025-12-20T10:00:00Z'
  },
  {
    id: 'proj-6',
    name: 'Data Analytics Pipeline',
    description: 'Big data processing and analytics infrastructure',
    icon: '📈',
    status: 'archived',
    type: 'data',
    ownerId: 'user-8',
    teamMembers: [
      {
        userId: 'user-8',
        name: 'David Kim',
        email: 'david.kim@specific-group.com',
        role: 'Data Engineer',
        accessLevel: 'owner',
        joinedAt: '2023-09-01T10:00:00Z'
      }
    ],
    aiAgents: ['developer', 'technical_writer'],
    integrations: {
      git: {
        platform: 'gitlab',
        url: 'https://gitlab.com/santander/data-pipeline',
        branch: 'main',
        connected: false
      }
    },
    techStack: {
      languages: ['Python', 'SQL'],
      frameworks: ['Apache Spark', 'Airflow'],
      databases: ['PostgreSQL', 'MongoDB'],
      tools: ['Jupyter', 'pytest']
    },
    stats: {
      totalWorkflows: 10,
      activeWorkflows: 0,
      completedWorkflows: 9,
      failedWorkflows: 1,
      teamSize: 1,
      aiAgentsCount: 2,
      filesGenerated: 67,
      linesOfCode: 15600
    },
    createdAt: '2023-09-01T10:00:00Z',
    updatedAt: '2024-12-01T10:00:00Z',
    lastActivity: '2024-11-15T10:00:00Z'
  }
];
