import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db_session
from src.api.schemas.settings import LlmSettings, LlmSettingsUpdate
from src.config import load_config
from src.db.models import AppSettings

router = APIRouter(prefix="/settings", dependencies=[Depends(get_current_user)])


@router.get("/llm", response_model=LlmSettings)
async def get_llm_settings(session: AsyncSession = Depends(get_db_session)) -> LlmSettings:
    result = await session.execute(select(AppSettings))
    settings = result.scalars().first()
    if settings:
        return LlmSettings.model_validate(settings)

    config = load_config()
    return LlmSettings(
        llm_base_url=os.getenv("OPENAI_API_BASE", "http://127.0.0.1:8080/v1"),
        llm_api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
        llm_model=os.getenv("OPENAI_API_MODEL", "devstral"),
        llm_timeout=config.llm_timeout,
    )


@router.put("/llm", response_model=LlmSettings)
async def update_llm_settings(
    request: LlmSettingsUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> LlmSettings:
    result = await session.execute(select(AppSettings))
    settings = result.scalars().first()
    now = datetime.utcnow()

    if settings:
        settings.llm_base_url = request.baseUrl
        settings.llm_api_key = request.apiKey
        settings.llm_model = request.model
        settings.llm_timeout = request.timeout
        settings.updated_at = now
    else:
        settings = AppSettings(
            id=uuid.uuid4(),
            llm_base_url=request.baseUrl,
            llm_api_key=request.apiKey,
            llm_model=request.model,
            llm_timeout=request.timeout,
            created_at=now,
            updated_at=now,
        )
        session.add(settings)

    await session.commit()
    await session.refresh(settings)
    return LlmSettings.model_validate(settings)
