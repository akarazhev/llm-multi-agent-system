/**
 * Mock data for agent communication
 */

import {
  AgentMessage,
  MessageType,
  MessageUrgency,
  MessageThread,
  ThreadStatus,
  AgentDecision,
  DecisionVariant,
  CommunicationStats
} from '../core/interfaces/agent-message.interface';
import { AgentRole } from '../core/interfaces/agent.interface';

/**
 * Mock messages for workflow_001 (Feature Development)
 */
export const MOCK_MESSAGES_WORKFLOW_001: AgentMessage[] = [
  // Initial requirements discussion
  {
    message_id: 'msg_001',
    workflow_id: 'workflow_001',
    agent_id: 'agent_ba_001',
    agent_name: 'Alice (BA)',
    agent_role: AgentRole.BUSINESS_ANALYST,
    message_type: MessageType.SYNCHRONIZATION,
    content: 'Starting requirements analysis for user authentication feature. I\'ll analyze the requirements and create user stories.',
    timestamp: '2024-01-15T10:00:00Z',
    addressed_to: ['all'],
    addressed_to_names: ['All Agents'],
    requires_response: false,
    urgency: MessageUrgency.MEDIUM,
    attachments: []
  },
  {
    message_id: 'msg_002',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.QUESTION,
    content: 'Alice, do we need to support OAuth providers (Google, GitHub) or just email/password authentication for MVP?',
    timestamp: '2024-01-15T10:15:00Z',
    addressed_to: ['agent_ba_001'],
    addressed_to_names: ['Alice (BA)'],
    requires_response: true,
    urgency: MessageUrgency.HIGH,
    parent_message_id: 'msg_001',
    attachments: []
  },
  {
    message_id: 'msg_003',
    workflow_id: 'workflow_001',
    agent_id: 'agent_ba_001',
    agent_name: 'Alice (BA)',
    agent_role: AgentRole.BUSINESS_ANALYST,
    message_type: MessageType.ANSWER,
    content: 'For MVP, let\'s start with email/password. OAuth providers can be added in Phase 2. Priority features:\n1. Email/password signup\n2. Email verification\n3. Password reset\n4. Session management',
    timestamp: '2024-01-15T10:20:00Z',
    addressed_to: ['agent_dev_001'],
    addressed_to_names: ['Bob (Developer)'],
    requires_response: false,
    urgency: MessageUrgency.HIGH,
    parent_message_id: 'msg_002',
    attachments: []
  },
  
  // Architecture discussion
  {
    message_id: 'msg_004',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.PROPOSAL,
    content: 'I propose using JWT for session management with the following approach:\n- Access tokens (15 min expiry)\n- Refresh tokens (7 days)\n- Token rotation on refresh\n\nWhat do you think?',
    timestamp: '2024-01-15T10:35:00Z',
    addressed_to: ['agent_devops_001', 'agent_security_001'],
    addressed_to_names: ['Charlie (DevOps)', 'Diana (Security)'],
    requires_response: true,
    urgency: MessageUrgency.MEDIUM,
    attachments: [
      {
        attachment_id: 'att_001',
        type: 'code',
        name: 'auth-flow.ts',
        language: 'typescript',
        content: `interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

async function login(email: string, password: string): Promise<TokenPair> {
  // Validate credentials
  // Generate tokens
  // Return token pair
}`
      }
    ]
  },
  {
    message_id: 'msg_005',
    workflow_id: 'workflow_001',
    agent_id: 'agent_security_001',
    agent_name: 'Diana (Security)',
    agent_role: AgentRole.SECURITY_ENGINEER,
    message_type: MessageType.ANSWER,
    content: 'JWT approach looks good. Additional security recommendations:\n1. Store refresh tokens in httpOnly cookies\n2. Implement token blacklist for logout\n3. Add rate limiting on auth endpoints\n4. Use bcrypt for password hashing (cost factor 12)',
    timestamp: '2024-01-15T10:45:00Z',
    addressed_to: ['agent_dev_001'],
    addressed_to_names: ['Bob (Developer)'],
    requires_response: false,
    urgency: MessageUrgency.MEDIUM,
    parent_message_id: 'msg_004',
    attachments: []
  },
  {
    message_id: 'msg_006',
    workflow_id: 'workflow_001',
    agent_id: 'agent_devops_001',
    agent_name: 'Charlie (DevOps)',
    agent_role: AgentRole.DEVOPS_ENGINEER,
    message_type: MessageType.ANSWER,
    content: 'Agreed with JWT. From infrastructure perspective:\n- Use Redis for token blacklist\n- Set up session monitoring\n- Configure token cleanup job\n\nI\'ll prepare the Redis configuration.',
    timestamp: '2024-01-15T10:50:00Z',
    addressed_to: ['agent_dev_001'],
    addressed_to_names: ['Bob (Developer)'],
    requires_response: false,
    urgency: MessageUrgency.MEDIUM,
    parent_message_id: 'msg_004',
    attachments: []
  },
  
  // Decision point
  {
    message_id: 'msg_007',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.DECISION,
    content: 'Decision: We\'ll implement JWT-based authentication with:\n- Access tokens (15 min) + Refresh tokens (7 days)\n- httpOnly cookies for refresh tokens\n- Redis-based token blacklist\n- bcrypt password hashing\n- Rate limiting on auth endpoints\n\nMoving to implementation phase.',
    timestamp: '2024-01-15T11:00:00Z',
    addressed_to: ['all'],
    addressed_to_names: ['All Agents'],
    requires_response: false,
    urgency: MessageUrgency.HIGH,
    parent_message_id: 'msg_004',
    attachments: []
  },
  
  // QA questions
  {
    message_id: 'msg_008',
    workflow_id: 'workflow_001',
    agent_id: 'agent_qa_001',
    agent_name: 'Eve (QA)',
    agent_role: AgentRole.QA_ENGINEER,
    message_type: MessageType.QUESTION,
    content: 'Bob, for testing strategy - should I focus on:\n1. Unit tests for auth functions\n2. Integration tests for token flow\n3. E2E tests for complete auth flow\n\nOr all of the above?',
    timestamp: '2024-01-15T11:15:00Z',
    addressed_to: ['agent_dev_001'],
    addressed_to_names: ['Bob (Developer)'],
    requires_response: true,
    urgency: MessageUrgency.MEDIUM,
    attachments: []
  },
  {
    message_id: 'msg_009',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.ANSWER,
    content: 'All three levels are important:\n1. Unit tests: auth service, password hashing, token generation\n2. Integration: full login/logout flow with Redis\n3. E2E: user signup → verification → login → protected routes\n\nPriority: E2E tests first to ensure critical path works.',
    timestamp: '2024-01-15T11:20:00Z',
    addressed_to: ['agent_qa_001'],
    addressed_to_names: ['Eve (QA)'],
    requires_response: false,
    urgency: MessageUrgency.MEDIUM,
    parent_message_id: 'msg_008',
    attachments: []
  },
  
  // Error/Blocker
  {
    message_id: 'msg_010',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.ERROR_REPORT,
    content: '⚠️ BLOCKER: Token refresh endpoint is failing in edge case when refresh token expires exactly during the refresh call. Need to handle race condition.',
    timestamp: '2024-01-15T14:30:00Z',
    addressed_to: ['agent_security_001'],
    addressed_to_names: ['Diana (Security)'],
    requires_response: true,
    urgency: MessageUrgency.CRITICAL,
    attachments: [
      {
        attachment_id: 'att_002',
        type: 'code',
        name: 'error-log.txt',
        content: 'TokenExpiredError: jwt expired at 2024-01-15T14:29:58.123Z'
      }
    ]
  },
  {
    message_id: 'msg_011',
    workflow_id: 'workflow_001',
    agent_id: 'agent_security_001',
    agent_name: 'Diana (Security)',
    agent_role: AgentRole.SECURITY_ENGINEER,
    message_type: MessageType.ANSWER,
    content: 'Good catch! Solution:\n1. Add 30-second grace period for refresh token validation\n2. Implement atomic token rotation with Redis WATCH\n3. Return clear error code (TOKEN_EXPIRED_REAUTH_REQUIRED) for client\n\nThis is a common pattern in OAuth2 implementations.',
    timestamp: '2024-01-15T14:35:00Z',
    addressed_to: ['agent_dev_001'],
    addressed_to_names: ['Bob (Developer)'],
    requires_response: false,
    urgency: MessageUrgency.CRITICAL,
    parent_message_id: 'msg_010',
    attachments: []
  },
  
  // Completion
  {
    message_id: 'msg_012',
    workflow_id: 'workflow_001',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.COMPLETION,
    content: '✅ Authentication implementation complete:\n- JWT auth with refresh tokens\n- Password hashing (bcrypt)\n- Redis token blacklist\n- Rate limiting\n- Grace period for token refresh\n\nReady for QA testing.',
    timestamp: '2024-01-15T16:00:00Z',
    addressed_to: ['agent_qa_001'],
    addressed_to_names: ['Eve (QA)'],
    requires_response: false,
    urgency: MessageUrgency.MEDIUM,
    attachments: [
      {
        attachment_id: 'att_003',
        type: 'link',
        name: 'Pull Request #123',
        url: 'https://github.com/project/repo/pull/123'
      }
    ]
  }
];

/**
 * Mock messages for workflow_002 (Bug Fix)
 */
export const MOCK_MESSAGES_WORKFLOW_002: AgentMessage[] = [
  {
    message_id: 'msg_201',
    workflow_id: 'workflow_002',
    agent_id: 'agent_qa_001',
    agent_name: 'Eve (QA)',
    agent_role: AgentRole.QA_ENGINEER,
    message_type: MessageType.ERROR_REPORT,
    content: '🐛 Critical Bug Found: Users can\'t reset password. Email service returns 500 error. Affects 100% of password reset attempts.',
    timestamp: '2024-01-14T09:00:00Z',
    addressed_to: ['agent_dev_001', 'agent_devops_001'],
    addressed_to_names: ['Bob (Developer)', 'Charlie (DevOps)'],
    requires_response: true,
    urgency: MessageUrgency.CRITICAL,
    attachments: [
      {
        attachment_id: 'att_201',
        type: 'code',
        name: 'error-trace.log',
        content: 'EmailServiceError: SMTP connection timeout at smtp.gmail.com:587'
      }
    ]
  },
  {
    message_id: 'msg_202',
    workflow_id: 'workflow_002',
    agent_id: 'agent_devops_001',
    agent_name: 'Charlie (DevOps)',
    agent_role: AgentRole.DEVOPS_ENGINEER,
    message_type: MessageType.ANSWER,
    content: 'Checking infrastructure... SMTP credentials expired yesterday. Rotating credentials now. ETA: 15 minutes.',
    timestamp: '2024-01-14T09:05:00Z',
    addressed_to: ['agent_qa_001', 'agent_dev_001'],
    addressed_to_names: ['Eve (QA)', 'Bob (Developer)'],
    requires_response: false,
    urgency: MessageUrgency.CRITICAL,
    parent_message_id: 'msg_201',
    attachments: []
  },
  {
    message_id: 'msg_203',
    workflow_id: 'workflow_002',
    agent_id: 'agent_dev_001',
    agent_name: 'Bob (Developer)',
    agent_role: AgentRole.DEVELOPER,
    message_type: MessageType.PROPOSAL,
    content: 'While Charlie fixes credentials, I suggest adding:\n1. Better error handling for email service failures\n2. Retry logic with exponential backoff\n3. Fallback to alternative email provider\n4. Alert monitoring for email service health',
    timestamp: '2024-01-14T09:10:00Z',
    addressed_to: ['agent_devops_001'],
    addressed_to_names: ['Charlie (DevOps)'],
    requires_response: true,
    urgency: MessageUrgency.HIGH,
    parent_message_id: 'msg_201',
    attachments: []
  },
  {
    message_id: 'msg_204',
    workflow_id: 'workflow_002',
    agent_id: 'agent_devops_001',
    agent_name: 'Charlie (DevOps)',
    agent_role: AgentRole.DEVOPS_ENGINEER,
    message_type: MessageType.COMPLETION,
    content: '✅ SMTP credentials rotated. Service is back online. Password reset working now. Let\'s implement Bob\'s suggestions to prevent future incidents.',
    timestamp: '2024-01-14T09:25:00Z',
    addressed_to: ['all'],
    addressed_to_names: ['All Agents'],
    requires_response: false,
    urgency: MessageUrgency.HIGH,
    attachments: []
  }
];

/**
 * Mock message threads
 */
export const MOCK_THREADS: { [workflow_id: string]: MessageThread[] } = {
  'workflow_001': [
    {
      root_message: MOCK_MESSAGES_WORKFLOW_001.find(m => m.message_id === 'msg_002')!,
      replies: MOCK_MESSAGES_WORKFLOW_001.filter(m => m.parent_message_id === 'msg_002'),
      status: ThreadStatus.RESOLVED,
      resolved_at: '2024-01-15T10:20:00Z',
      resolved_by: 'agent_ba_001'
    },
    {
      root_message: MOCK_MESSAGES_WORKFLOW_001.find(m => m.message_id === 'msg_004')!,
      replies: MOCK_MESSAGES_WORKFLOW_001.filter(m => m.parent_message_id === 'msg_004'),
      status: ThreadStatus.RESOLVED,
      resolved_at: '2024-01-15T11:00:00Z',
      resolved_by: 'agent_dev_001',
      decision: 'JWT-based authentication with refresh tokens and Redis blacklist'
    },
    {
      root_message: MOCK_MESSAGES_WORKFLOW_001.find(m => m.message_id === 'msg_008')!,
      replies: MOCK_MESSAGES_WORKFLOW_001.filter(m => m.parent_message_id === 'msg_008'),
      status: ThreadStatus.RESOLVED,
      resolved_at: '2024-01-15T11:20:00Z',
      resolved_by: 'agent_dev_001'
    },
    {
      root_message: MOCK_MESSAGES_WORKFLOW_001.find(m => m.message_id === 'msg_010')!,
      replies: MOCK_MESSAGES_WORKFLOW_001.filter(m => m.parent_message_id === 'msg_010'),
      status: ThreadStatus.RESOLVED,
      resolved_at: '2024-01-15T14:35:00Z',
      resolved_by: 'agent_security_001'
    }
  ],
  'workflow_002': [
    {
      root_message: MOCK_MESSAGES_WORKFLOW_002.find(m => m.message_id === 'msg_201')!,
      replies: MOCK_MESSAGES_WORKFLOW_002.filter(m => m.parent_message_id === 'msg_201'),
      status: ThreadStatus.RESOLVED,
      resolved_at: '2024-01-14T09:25:00Z',
      resolved_by: 'agent_devops_001'
    }
  ]
};

/**
 * Mock decisions
 */
export const MOCK_DECISIONS: AgentDecision[] = [
  {
    decision_id: 'dec_001',
    workflow_id: 'workflow_001',
    problem: 'Session Management Strategy',
    description: 'Choose between JWT, server-side sessions, or hybrid approach for user authentication',
    timestamp: '2024-01-15T11:00:00Z',
    variants: [
      {
        variant_id: 'var_001',
        name: 'JWT with Refresh Tokens',
        description: 'Stateless JWT for access, refresh tokens with Redis blacklist',
        proposed_by: 'agent_dev_001',
        proposed_by_name: 'Bob (Developer)',
        pros: [
          'Stateless - scales horizontally',
          'No database lookup per request',
          'Standard industry practice',
          'Works with microservices'
        ],
        cons: [
          'Cannot revoke access tokens before expiry',
          'Requires Redis for blacklist',
          'Token size in headers'
        ]
      },
      {
        variant_id: 'var_002',
        name: 'Server-Side Sessions',
        description: 'Traditional session storage with session ID in cookie',
        proposed_by: 'agent_security_001',
        proposed_by_name: 'Diana (Security)',
        pros: [
          'Easy to revoke',
          'Small cookie size',
          'Simple implementation',
          'Better security control'
        ],
        cons: [
          'Database lookup per request',
          'Harder to scale',
          'Session store required',
          'Not ideal for microservices'
        ]
      }
    ],
    chosen_variant_id: 'var_001',
    votes: {
      'agent_dev_001': 'var_001',
      'agent_security_001': 'var_001',
      'agent_devops_001': 'var_001',
      'agent_ba_001': 'var_001'
    },
    justification: 'JWT approach chosen for better scalability and microservices compatibility. Security concerns addressed with refresh token rotation and Redis blacklist.',
    responsible_agents: ['agent_dev_001', 'agent_devops_001'],
    discussion_thread_id: 'msg_004'
  }
];

/**
 * Mock communication stats
 */
export const MOCK_COMMUNICATION_STATS: { [workflow_id: string]: CommunicationStats } = {
  'workflow_001': {
    total_messages: 12,
    messages_by_type: {
      [MessageType.QUESTION]: 3,
      [MessageType.PROPOSAL]: 2,
      [MessageType.ANSWER]: 4,
      [MessageType.DECISION]: 1,
      [MessageType.SYNCHRONIZATION]: 1,
      [MessageType.ERROR_REPORT]: 1,
      [MessageType.COMPLETION]: 1
    },
    messages_by_agent: {
      'agent_ba_001': 2,
      'agent_dev_001': 6,
      'agent_qa_001': 2,
      'agent_devops_001': 1,
      'agent_security_001': 2
    },
    threads_count: 4,
    open_threads: 0,
    resolved_threads: 4,
    decisions_count: 1,
    average_response_time_seconds: 180
  },
  'workflow_002': {
    total_messages: 4,
    messages_by_type: {
      [MessageType.ERROR_REPORT]: 1,
      [MessageType.ANSWER]: 1,
      [MessageType.PROPOSAL]: 1,
      [MessageType.COMPLETION]: 1
    },
    messages_by_agent: {
      'agent_qa_001': 1,
      'agent_dev_001': 1,
      'agent_devops_001': 2
    },
    threads_count: 1,
    open_threads: 0,
    resolved_threads: 1,
    decisions_count: 0,
    average_response_time_seconds: 300
  }
};

/**
 * Helper function to get messages for a workflow
 */
export function getMessagesForWorkflow(workflowId: string): AgentMessage[] {
  switch (workflowId) {
    case 'workflow_001':
      return MOCK_MESSAGES_WORKFLOW_001;
    case 'workflow_002':
      return MOCK_MESSAGES_WORKFLOW_002;
    default:
      return [];
  }
}

/**
 * Helper function to get threads for a workflow
 */
export function getThreadsForWorkflow(workflowId: string): MessageThread[] {
  return MOCK_THREADS[workflowId] || [];
}

/**
 * Helper function to get decisions for a workflow
 */
export function getDecisionsForWorkflow(workflowId: string): AgentDecision[] {
  return MOCK_DECISIONS.filter(d => d.workflow_id === workflowId);
}

/**
 * Helper function to get communication stats for a workflow
 */
export function getCommunicationStats(workflowId: string): CommunicationStats {
  return MOCK_COMMUNICATION_STATS[workflowId] || {
    total_messages: 0,
    messages_by_type: {},
    messages_by_agent: {},
    threads_count: 0,
    open_threads: 0,
    resolved_threads: 0,
    decisions_count: 0,
    average_response_time_seconds: 0
  };
}
