from app.graph.repository import KnowledgeRepository
from app.models.chat import ChatResponse
from app.models.common import Citation
from .context_builder import build_context


class RagPipeline:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def answer(self, question: str, limit: int = 5) -> ChatResponse:
        results = self.repository.search(question, limit)
        if not results:
            return ChatResponse(answer="I couldn't find supporting evidence in the connected knowledge yet.", citations=[], grounded=False)
        context = build_context(results)
        answer = f"Based on the available company knowledge:\n\n{context}"
        citations = [Citation(id=r.id, title=r.title, source=r.source, url=r.url) for r in results]
        return ChatResponse(answer=answer, citations=citations, grounded=True)
