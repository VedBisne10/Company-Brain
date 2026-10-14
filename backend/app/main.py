from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, graph, health, integrations, search
from app.api.webhooks import github, google, slack
from app.config.settings import get_settings
from app.graph.repository import KnowledgeRepository
from app.rag.pipeline import RagPipeline
from app.services.chat_service import ChatService
from app.services.graph_service import GraphService
from app.services.search_service import SearchService


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    repository = KnowledgeRepository()
    app.state.settings = settings
    app.state.repository = repository
    app.state.search_service = SearchService(repository)
    app.state.graph_service = GraphService(repository)
    app.state.chat_service = ChatService(RagPipeline(repository))
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(chat.router, prefix=settings.api_prefix)
    app.include_router(search.router, prefix=settings.api_prefix)
    app.include_router(graph.router, prefix=settings.api_prefix)
    app.include_router(integrations.router, prefix=settings.api_prefix)
    app.include_router(github.router, prefix=settings.api_prefix)
    app.include_router(slack.router, prefix=settings.api_prefix)
    app.include_router(google.router, prefix=settings.api_prefix)
    return app


app = create_app()
