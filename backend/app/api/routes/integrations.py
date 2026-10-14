from fastapi import APIRouter, Request

from app.models.graph import IntegrationStatus

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("", response_model=list[IntegrationStatus])
def integrations(request: Request):
    settings = request.app.state.settings
    return [
        IntegrationStatus(provider="github", connected=False, configured=bool(settings.github_webhook_secret)),
        IntegrationStatus(provider="slack", connected=False, configured=bool(settings.slack_signing_secret)),
        IntegrationStatus(provider="google", connected=False, configured=False),
    ]
