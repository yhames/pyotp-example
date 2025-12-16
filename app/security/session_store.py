# app/security/session_store.py
import secrets
import time
from typing import Optional

from cachetools import TTLCache

from app.config import get_settings
from app.model import SessionStore

settings = get_settings()

# maxsize는 admin 세션 수 기준 (넉넉히)
_sessions = TTLCache(maxsize=1024, ttl=settings.session_ttl)


def create_session(ip: str) -> str:
    # 고유한 세션 ID 생성
    session_id = secrets.token_urlsafe(32)

    # 세션 저장
    now = time.time()
    _sessions[session_id] = SessionStore(ip=ip, created_at=now, last_access=now)
    return session_id


def get_session(session_id: str, ip: str) -> Optional[SessionStore]:
    now = time.time()
    session: Optional[SessionStore] = _sessions.get(session_id)
    if not session:
        return None

    # absolute timeout
    if now - session.created_at > settings.session_absolute_timeout:
        _sessions.pop(session_id, None)
        return None

    # idle timeout
    if now - session.last_access > settings.session_idle_timeout:
        _sessions.pop(session_id, None)
        return None

    # IP binding
    if session.ip != ip:
        return None

    return session


def touch_session(session_id: str):
    session = _sessions.get(session_id)
    if session:
        session.last_access = time.time()


def revoke_session(session_id: str):
    _sessions.pop(session_id, None)
