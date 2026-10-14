from app.graph.repository import KnowledgeRepository
from app.models.common import KnowledgeRecord
from .chunker import chunk_text


class IngestionPipeline:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def ingest(self, record: KnowledgeRecord) -> dict[str, int | bool | str]:
        created = self.repository.upsert(record)
        chunks = chunk_text(record.content)
        for index, chunk in enumerate(chunks):
            self.repository.upsert(record.model_copy(update={"id": f"{record.id}:chunk:{index}", "title": f"{record.title} (chunk {index + 1})", "content": chunk, "relationships": [record.id]}))
        return {"id": record.id, "created": created, "chunks": len(chunks)}
