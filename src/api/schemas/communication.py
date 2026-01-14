from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class MessageAttachment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    attachment_id: str
    type: str
    name: str
    content: Optional[str] = None
    url: Optional[str] = None
    language: Optional[str] = None
    size: Optional[int] = None


class AgentMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message_id: str
    workflow_id: str
    agent_id: Optional[str] = None
    agent_name: str
    agent_role: str
    message_type: str
    content: str
    timestamp: str
    addressed_to: Optional[List[str]] = None
    addressed_to_names: Optional[List[str]] = None
    parent_message_id: Optional[str] = None
    reply_count: Optional[int] = None
    requires_response: bool
    urgency: str
    attachments: Optional[List[MessageAttachment]] = None
    is_edited: Optional[bool] = None
    edited_at: Optional[str] = None


class MessageThread(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    root_message: AgentMessage
    replies: List[AgentMessage]
    status: str
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    decision: Optional[str] = None


class DecisionVariant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    variant_id: str
    name: str
    description: str
    proposed_by: str
    proposed_by_name: str
    pros: List[str]
    cons: List[str]


class AgentDecision(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    decision_id: str
    workflow_id: str
    problem: str
    description: str
    timestamp: str
    variants: List[DecisionVariant]
    chosen_variant_id: str
    votes: Dict[str, str]
    justification: str
    responsible_agents: List[str]
    discussion_thread_id: Optional[str] = None


class CommunicationStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_messages: int
    messages_by_type: Dict[str, int]
    messages_by_agent: Dict[str, int]
    threads_count: int
    open_threads: int
    resolved_threads: int
    decisions_count: int
    average_response_time_seconds: int


class CreateMessageRequest(BaseModel):
    agent_id: Optional[str] = None
    agent_name: str
    agent_role: str
    message_type: str
    content: str
    addressed_to: Optional[List[str]] = None
    addressed_to_names: Optional[List[str]] = None
    parent_message_id: Optional[str] = None
    requires_response: bool = False
    urgency: str = "medium"
    attachments: Optional[List[MessageAttachment]] = None
