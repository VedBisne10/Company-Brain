from app.graph.repository import KnowledgeRepository


class SearchService:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def search(self, query: str, limit: int = 10):
        return self.repository.search(query, limit)
