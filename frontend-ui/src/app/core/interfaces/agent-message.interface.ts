/**
 * Agent Communication Interfaces
 * For inter-agent communication within workflows
 */

import { AgentRole } from './agent.interface';

/**
 * Type of agent message
 */
export enum MessageType {
  QUESTION = 'question',           // Requires response from specific agents
  PROPOSAL = 'proposal',           // Requires discussion and agreement
  ANSWER = 'answer',               // Response to a question
  DECISION = 'decision',           // Final decision after discussion
  CLARIFICATION = 'clarification', // Clarification without waiting for response
  SYNCHRONIZATION = 'synchronization', // Status update
  ERROR_REPORT = 'error_report',   // Error or blocker notification
  COMPLETION = 'completion'        // Task completion notification
}

/**
 * Urgency level of the message
 */
export enum MessageUrgency {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

/**
 * Status of a message thread
 */
export enum ThreadStatus {
  OPEN = 'open',
  RESOLVED = 'resolved',
  BLOCKED = 'blocked'
}

/**
 * Attachment to a message (code snippet, file, link)
 */
export interface MessageAttachment {
  attachment_id: string;
  type: 'code' | 'file' | 'link' | 'image';
  name: string;
  content?: string;
  url?: string;
  language?: string; // For code attachments
  size?: number;
}

/**
 * Agent message in a workflow
 */
export interface AgentMessage {
  message_id: string;
  workflow_id: string;
  agent_id: string;
  agent_name: string;
  agent_role: AgentRole;
  message_type: MessageType;
  content: string;
  timestamp: string;
  
  // Addressing
  addressed_to?: string[]; // Agent IDs or 'all'
  addressed_to_names?: string[]; // Agent names for display
  
  // Threading
  parent_message_id?: string;
  reply_count?: number;
  
  // Response management
  requires_response: boolean;
  urgency: MessageUrgency;
  
  // Attachments
  attachments?: MessageAttachment[];
  
  // Status
  is_edited?: boolean;
  edited_at?: string;
}

/**
 * Message thread (parent message + replies)
 */
export interface MessageThread {
  root_message: AgentMessage;
  replies: AgentMessage[];
  status: ThreadStatus;
  resolved_at?: string;
  resolved_by?: string;
  decision?: string; // Final decision if thread resulted in one
}

/**
 * Decision made by agents
 */
export interface AgentDecision {
  decision_id: string;
  workflow_id: string;
  problem: string;
  description: string;
  timestamp: string;
  
  // Variants considered
  variants: DecisionVariant[];
  
  // Chosen variant
  chosen_variant_id: string;
  
  // Voting
  votes: { [agent_id: string]: string }; // agent_id -> variant_id
  
  // Justification
  justification: string;
  responsible_agents: string[]; // Agents responsible for implementation
  
  // Related messages
  discussion_thread_id?: string;
}

/**
 * Decision variant/option
 */
export interface DecisionVariant {
  variant_id: string;
  name: string;
  description: string;
  proposed_by: string; // Agent ID
  proposed_by_name: string; // Agent name
  pros: string[];
  cons: string[];
}

/**
 * Communication statistics for a workflow
 */
export interface CommunicationStats {
  total_messages: number;
  messages_by_type: { [key in MessageType]?: number };
  messages_by_agent: { [agent_id: string]: number };
  threads_count: number;
  open_threads: number;
  resolved_threads: number;
  decisions_count: number;
  average_response_time_seconds: number;
}
