from app.graph.repository import KnowledgeRepository


class GraphService:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def explore(self, entity_id: str | None = None, limit: int = 50):
        return self.repository.graph(entity_id, limit)
