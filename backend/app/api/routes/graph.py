from fastapi import APIRouter, Query, Request

from app.models.common import GraphData

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("", response_model=GraphData)
def graph(request: Request, entity_id: str | None = None, limit: int = Query(default=50, ge=1, le=500)):
    return request.app.state.graph_service.explore(entity_id, limit)
