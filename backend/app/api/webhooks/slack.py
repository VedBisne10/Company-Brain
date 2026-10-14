from fastapi import APIRouter, Header, HTTPException, Request

from app.ingestion.normalizer import normalize_record
from app.models.common import Source
from app.utils.security import verify_signature

router = APIRouter(prefix="/webhooks/slack", tags=["webhooks"])


@router.post("")
async def slack_webhook(request: Request, x_slack_signature: str | None = Header(default=None)):
    body = await request.body()
    secret = request.app.state.settings.slack_signing_secret
    if secret and not verify_signature(body, x_slack_signature, secret, prefix="v0="):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}
    event = payload.get("event", payload)
    record = normalize_record(event, Source.slack, kind="message")
    created = request.app.state.repository.upsert(record)
    return {"accepted": True, "created": created, "id": record.id}
