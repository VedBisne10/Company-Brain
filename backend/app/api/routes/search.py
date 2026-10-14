from fastapi import APIRouter, Query, Request

from app.models.common import SearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
def search(request: Request, q: str = Query(min_length=1), limit: int = Query(default=10, ge=1, le=50)):
    return request.app.state.search_service.search(q, limit)
