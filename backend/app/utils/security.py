import hashlib
import hmac


def verify_signature(payload: bytes, signature: str | None, secret: str | None, prefix: str = "sha256=") -> bool:
    if not secret or not signature:
        return False
    expected = prefix + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
