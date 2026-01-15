import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select

from src.config import load_config
from src.db.database import async_session
from src.db.models import AppSettings


@dataclass
class LlmSettingsData:
    base_url: str
    api_key: str
    model: str
    timeout: int


class SettingsService:
    def __init__(self, cache_ttl_seconds: int = 30) -> None:
        self._cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self._cached_at: Optional[datetime] = None
        self._cached_settings: Optional[LlmSettingsData] = None

    async def get_llm_settings(self) -> LlmSettingsData:
        if self._cached_settings and self._cached_at:
            if datetime.utcnow() - self._cached_at < self._cache_ttl:
                return self._cached_settings

        settings = await self._load_from_db()
        if settings is None:
            settings = self._load_defaults()

        self._cached_settings = settings
        self._cached_at = datetime.utcnow()
        return settings

    async def _load_from_db(self) -> Optional[LlmSettingsData]:
        async with async_session() as session:
            result = await session.execute(select(AppSettings))
            row = result.scalars().first()
            if not row:
                return None
            return LlmSettingsData(
                base_url=row.llm_base_url,
                api_key=row.llm_api_key or "",
                model=row.llm_model or "devstral",
                timeout=row.llm_timeout or load_config().llm_timeout,
            )

    def _load_defaults(self) -> LlmSettingsData:
        config = load_config()
        return LlmSettingsData(
            base_url=os.getenv("OPENAI_API_BASE", "http://127.0.0.1:8080/v1"),
            api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
            model=os.getenv("OPENAI_API_MODEL", "devstral"),
            timeout=config.llm_timeout,
        )


settings_service = SettingsService()
