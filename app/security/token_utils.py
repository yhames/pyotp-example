from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.model import SessionStore
from app.security.session_store import get_session, touch_session

security = HTTPBearer()


def require_admin_token(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> SessionStore:
    return _validate_admin_session(
        request=request,
        credentials=credentials,
        touch=True,
    )


def require_admin_token_no_touch(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> SessionStore:
    return _validate_admin_session(
        request=request,
        credentials=credentials,
        touch=False,
    )


def _validate_admin_session(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        touch: bool = True  # 세션 접근 시점 갱신 여부
) -> SessionStore:
    session_id = credentials.credentials
    client_ip = request.client.host

    session = get_session(session_id, client_ip)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    if touch:
        touch_session(session_id)
    return session
