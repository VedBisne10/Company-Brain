from fastapi import APIRouter, Request

from app.models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request):
    return request.app.state.chat_service.ask(payload)
