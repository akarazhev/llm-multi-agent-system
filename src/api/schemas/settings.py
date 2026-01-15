from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LlmSettings(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    baseUrl: str = Field(alias="llm_base_url")
    apiKey: Optional[str] = Field(default=None, alias="llm_api_key")
    model: Optional[str] = Field(default=None, alias="llm_model")
    timeout: Optional[int] = Field(default=None, alias="llm_timeout")


class LlmSettingsUpdate(BaseModel):
    baseUrl: str
    apiKey: Optional[str] = None
    model: Optional[str] = None
    timeout: Optional[int] = None
