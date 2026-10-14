"""Signed, expiring authentication tickets for the VPS control center."""
import base64
import hashlib
import hmac
import json
import time
from secrets import token_urlsafe


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def create_ticket(user_id: int, secret: str, ttl: int = 900) -> str:
    if not secret or len(secret) < 32:
        raise ValueError("WEBPANEL_SECRET must contain at least 32 characters")
    payload = {"uid": int(user_id), "exp": int(time.time()) + max(60, min(int(ttl), 1800)), "nonce": token_urlsafe(12)}
    body = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
    return f"{body}.{_b64(signature)}"


def verify_ticket(ticket: str, secret: str, allowed_ids) -> dict | None:
    if not secret or not isinstance(ticket, str) or len(ticket) > 2048:
        return None
    try:
        body, supplied = ticket.split(".", 1)
        expected = _b64(hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(supplied, expected):
            return None
        raw = base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))
        payload = json.loads(raw.decode("utf-8"))
        uid, exp = int(payload["uid"]), int(payload["exp"])
        if exp <= int(time.time()) or uid not in {int(x) for x in allowed_ids}:
            return None
        return {"uid": uid, "exp": exp}
    except (ValueError, TypeError, KeyError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def parse_admin_ids(owner_id, sudo_users="") -> set[int]:
    ids = set()
    try:
        if int(owner_id or 0) > 0:
            ids.add(int(owner_id))
    except (ValueError, TypeError):
        pass
    values = sudo_users if isinstance(sudo_users, (list, tuple, set)) else str(sudo_users or "").replace(" ", "").split(",")
    for value in values:
        try:
            if str(value).strip():
                ids.add(int(value))
        except (ValueError, TypeError):
            continue
    return ids
