from app.models.chat import ChatRequest
from app.rag.pipeline import RagPipeline


class ChatService:
    def __init__(self, pipeline: RagPipeline) -> None:
        self.pipeline = pipeline

    def ask(self, request: ChatRequest):
        return self.pipeline.answer(request.question, request.limit)
