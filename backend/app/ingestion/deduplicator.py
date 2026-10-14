import hashlib

from app.models.common import KnowledgeRecord


def content_hash(record: KnowledgeRecord) -> str:
    value = f"{record.id}\0{record.title}\0{record.content}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
