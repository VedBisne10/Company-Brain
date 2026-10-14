from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Source(str, Enum):
    github = "github"
    slack = "slack"
    google = "google"
    manual = "manual"


class KnowledgeRecord(BaseModel):
    id: str
    source: Source
    kind: str
    title: str = ""
    content: str = ""
    url: str | None = None
    author: str | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
    relationships: list[str] = Field(default_factory=list)


class SearchResult(BaseModel):
    id: str
    title: str
    snippet: str
    source: Source
    url: str | None = None
    score: float


class Citation(BaseModel):
    id: str
    title: str
    source: Source
    url: str | None = None


class GraphNode(BaseModel):
    id: str
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str


class GraphData(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
