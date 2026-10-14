from typing import Any

from app.models.common import KnowledgeRecord, Source


def normalize_record(payload: dict[str, Any], source: Source, *, kind: str | None = None) -> KnowledgeRecord:
    record_id = str(payload.get("id") or payload.get("source_id") or payload.get("ts") or "unknown")
    return KnowledgeRecord(
        id=f"{source.value}:{record_id}",
        source=source,
        kind=kind or str(payload.get("kind") or payload.get("type") or "document"),
        title=str(payload.get("title") or payload.get("name") or payload.get("text", "")[:80]),
        content=str(payload.get("content") or payload.get("text") or payload.get("body") or ""),
        url=payload.get("url") or payload.get("html_url") or payload.get("permalink"),
        author=payload.get("author") or payload.get("user") or payload.get("user_name"),
        metadata={k: v for k, v in payload.items() if k not in {"content", "text", "body"}},
        relationships=[str(item) for item in payload.get("relationships", [])],
    )
