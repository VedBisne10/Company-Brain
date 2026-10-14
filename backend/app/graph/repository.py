from collections import defaultdict
import re
from typing import Iterable

from app.models.common import GraphData, GraphEdge, GraphNode, KnowledgeRecord, SearchResult
from app.ingestion.deduplicator import content_hash


class KnowledgeRepository:
    """Small repository abstraction; replace its storage adapter with FalkorDB in production."""

    def __init__(self) -> None:
        self.records: dict[str, KnowledgeRecord] = {}
        self.hashes: dict[str, str] = {}
        self.edges: set[tuple[str, str, str]] = set()

    def upsert(self, record: KnowledgeRecord) -> bool:
        created = record.id not in self.records
        self.records[record.id] = record
        self.hashes[record.id] = content_hash(record)
        for related in record.relationships:
            self.edges.add((record.id, related, "RELATED_TO"))
        return created

    def upsert_many(self, records: Iterable[KnowledgeRecord]) -> int:
        return sum(self.upsert(record) for record in records)

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        terms = set(re.findall(r"[\w-]+", query.lower()))
        scored: list[SearchResult] = []
        for record in self.records.values():
            haystack = f"{record.title} {record.content} {record.author or ''}".lower()
            score = sum(haystack.count(term) for term in terms)
            if score:
                pos = min((haystack.find(term) for term in terms if term in haystack), default=0)
                snippet = record.content[max(0, pos - 80):pos + 240].strip()
                scored.append(SearchResult(id=record.id, title=record.title, snippet=snippet, source=record.source, url=record.url, score=float(score)))
        return sorted(scored, key=lambda item: (-item.score, item.title))[:limit]

    def graph(self, entity_id: str | None = None, limit: int = 50) -> GraphData:
        ids = {entity_id} if entity_id else set(self.records)
        selected = [self.records[item] for item in ids if item in self.records][:limit]
        nodes = [GraphNode(id=r.id, label=r.title or r.kind, properties={"source": r.source.value, "kind": r.kind, "url": r.url}) for r in selected]
        allowed = {n.id for n in nodes}
        edges = [GraphEdge(source=a, target=b, type=t) for a, b, t in self.edges if a in allowed and b in allowed]
        return GraphData(nodes=nodes, edges=edges)

    def clear(self) -> None:
        self.records.clear(); self.hashes.clear(); self.edges.clear()
