from fastapi import APIRouter

router = APIRouter(prefix="/webhooks/google", tags=["webhooks"])


@router.post("")
def google_webhook() -> dict[str, bool]:
    return {"accepted": True}
