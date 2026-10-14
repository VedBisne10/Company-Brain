from typing import Any

from pydantic import BaseModel, Field


class GraphQuery(BaseModel):
    entity_id: str | None = None
    limit: int = Field(default=50, ge=1, le=500)


class UpsertResult(BaseModel):
    id: str
    created: bool
    chunks: int = 0


class IntegrationStatus(BaseModel):
    provider: str
    connected: bool
    configured: bool
    details: dict[str, Any] = Field(default_factory=dict)
