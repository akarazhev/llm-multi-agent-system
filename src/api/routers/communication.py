import uuid
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.communication import (
    AgentDecision,
    AgentMessage,
    CommunicationStats,
    CreateMessageRequest,
    MessageThread,
)
from src.db.models import AgentMessage as AgentMessageModel
from src.db.models import Decision as DecisionModel


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/{workflow_id}/messages", response_model=list[AgentMessage])
async def list_messages(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> list[AgentMessage]:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(
        select(AgentMessageModel)
        .where(AgentMessageModel.workflow_id == workflow_uuid)
        .order_by(AgentMessageModel.created_at)
    )
    messages = result.scalars().all()
    return [
        AgentMessage(
            message_id=str(message.message_id),
            workflow_id=str(message.workflow_id),
            agent_id=str(message.agent_id) if message.agent_id else None,
            agent_name=message.agent_name,
            agent_role=message.agent_role,
            message_type=message.message_type,
            content=message.content,
            timestamp=message.created_at.isoformat(),
            addressed_to=message.addressed_to,
            addressed_to_names=message.addressed_to_names,
            parent_message_id=str(message.parent_message_id) if message.parent_message_id else None,
            requires_response=message.requires_response,
            urgency=message.urgency,
            attachments=message.attachments,
            is_edited=message.is_edited,
            edited_at=message.edited_at.isoformat() if message.edited_at else None,
        )
        for message in messages
    ]


@router.post("/{workflow_id}/messages", response_model=AgentMessage)
async def create_message(
    workflow_id: str,
    request: CreateMessageRequest,
    session: AsyncSession = Depends(get_db_session),
) -> AgentMessage:
    workflow_uuid = uuid.UUID(workflow_id)
    message = AgentMessageModel(
        message_id=uuid.uuid4(),
        workflow_id=workflow_uuid,
        agent_id=request.agent_id,
        agent_name=request.agent_name,
        agent_role=request.agent_role,
        message_type=request.message_type,
        content=request.content,
        addressed_to=request.addressed_to or [],
        addressed_to_names=request.addressed_to_names or [],
        parent_message_id=request.parent_message_id,
        requires_response=request.requires_response,
        urgency=request.urgency,
        attachments=[attachment.model_dump() for attachment in request.attachments] if request.attachments else [],
        is_edited=False,
        edited_at=None,
        created_at=datetime.utcnow(),
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return AgentMessage(
        message_id=str(message.message_id),
        workflow_id=str(message.workflow_id),
        agent_id=str(message.agent_id) if message.agent_id else None,
        agent_name=message.agent_name,
        agent_role=message.agent_role,
        message_type=message.message_type,
        content=message.content,
        timestamp=message.created_at.isoformat(),
        addressed_to=message.addressed_to,
        addressed_to_names=message.addressed_to_names,
        parent_message_id=str(message.parent_message_id) if message.parent_message_id else None,
        requires_response=message.requires_response,
        urgency=message.urgency,
        attachments=message.attachments,
        is_edited=message.is_edited,
        edited_at=message.edited_at.isoformat() if message.edited_at else None,
    )


@router.get("/{workflow_id}/threads", response_model=list[MessageThread])
async def list_threads(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> list[MessageThread]:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(
        select(AgentMessageModel)
        .where(AgentMessageModel.workflow_id == workflow_uuid)
        .order_by(AgentMessageModel.created_at)
    )
    messages = result.scalars().all()
    roots = [m for m in messages if m.parent_message_id is None]
    replies_by_parent: Dict[str, List[AgentMessageModel]] = {}
    for message in messages:
        if message.parent_message_id:
            replies_by_parent.setdefault(str(message.parent_message_id), []).append(message)

    threads: List[MessageThread] = []
    for root in roots:
        replies = replies_by_parent.get(str(root.message_id), [])
        threads.append(
            MessageThread(
                root_message=AgentMessage(
                    message_id=str(root.message_id),
                    workflow_id=str(root.workflow_id),
                    agent_id=str(root.agent_id) if root.agent_id else None,
                    agent_name=root.agent_name,
                    agent_role=root.agent_role,
                    message_type=root.message_type,
                    content=root.content,
                    timestamp=root.created_at.isoformat(),
                    addressed_to=root.addressed_to,
                    addressed_to_names=root.addressed_to_names,
                    parent_message_id=None,
                    requires_response=root.requires_response,
                    urgency=root.urgency,
                    attachments=root.attachments,
                    is_edited=root.is_edited,
                    edited_at=root.edited_at.isoformat() if root.edited_at else None,
                ),
                replies=[
                    AgentMessage(
                        message_id=str(reply.message_id),
                        workflow_id=str(reply.workflow_id),
                        agent_id=str(reply.agent_id) if reply.agent_id else None,
                        agent_name=reply.agent_name,
                        agent_role=reply.agent_role,
                        message_type=reply.message_type,
                        content=reply.content,
                        timestamp=reply.created_at.isoformat(),
                        addressed_to=reply.addressed_to,
                        addressed_to_names=reply.addressed_to_names,
                        parent_message_id=str(reply.parent_message_id) if reply.parent_message_id else None,
                        requires_response=reply.requires_response,
                        urgency=reply.urgency,
                        attachments=reply.attachments,
                        is_edited=reply.is_edited,
                        edited_at=reply.edited_at.isoformat() if reply.edited_at else None,
                    )
                    for reply in replies
                ],
                status="open",
            )
        )
    return threads


@router.get("/{workflow_id}/decisions", response_model=list[AgentDecision])
async def list_decisions(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> list[AgentDecision]:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(DecisionModel).where(DecisionModel.workflow_id == workflow_uuid))
    decisions = result.scalars().all()
    return [
        AgentDecision(
            decision_id=str(decision.decision_id),
            workflow_id=str(decision.workflow_id),
            problem=decision.problem,
            description=decision.description or "",
            timestamp=decision.created_at.isoformat(),
            variants=decision.variants or [],
            chosen_variant_id=decision.chosen_variant_id or "",
            votes=decision.votes or {},
            justification=decision.justification or "",
            responsible_agents=decision.responsible_agents or [],
            discussion_thread_id=str(decision.discussion_thread_id) if decision.discussion_thread_id else None,
        )
        for decision in decisions
    ]


@router.get("/{workflow_id}/stats", response_model=CommunicationStats)
async def get_stats(workflow_id: str, session: AsyncSession = Depends(get_db_session)) -> CommunicationStats:
    workflow_uuid = uuid.UUID(workflow_id)
    result = await session.execute(select(AgentMessageModel).where(AgentMessageModel.workflow_id == workflow_uuid))
    messages = result.scalars().all()
    result_decisions = await session.execute(select(DecisionModel).where(DecisionModel.workflow_id == workflow_uuid))
    decisions = result_decisions.scalars().all()

    messages_by_type: Dict[str, int] = {}
    messages_by_agent: Dict[str, int] = {}
    for message in messages:
        messages_by_type[message.message_type] = messages_by_type.get(message.message_type, 0) + 1
        if message.agent_id:
            agent_id = str(message.agent_id)
            messages_by_agent[agent_id] = messages_by_agent.get(agent_id, 0) + 1

    threads_count = len([m for m in messages if m.parent_message_id is None])

    return CommunicationStats(
        total_messages=len(messages),
        messages_by_type=messages_by_type,
        messages_by_agent=messages_by_agent,
        threads_count=threads_count,
        open_threads=threads_count,
        resolved_threads=0,
        decisions_count=len(decisions),
        average_response_time_seconds=0,
    )
