from fastapi import APIRouter, Header, HTTPException, Request

from app.ingestion.normalizer import normalize_record
from app.models.common import Source
from app.utils.security import verify_signature

router = APIRouter(prefix="/webhooks/github", tags=["webhooks"])


@router.post("")
async def github_webhook(request: Request, x_hub_signature_256: str | None = Header(default=None)):
    body = await request.body()
    secret = request.app.state.settings.github_webhook_secret
    if secret and not verify_signature(body, x_hub_signature_256, secret):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")
    payload = await request.json()
    event = request.headers.get("x-github-event", "unknown")
    record = normalize_record({**payload, "kind": event}, Source.github)
    result = request.app.state.repository.upsert(record)
    return {"accepted": True, "event": event, "created": result, "id": record.id}
