from fastapi import APIRouter, Depends

from app.model import SessionStore
from app.security.token_utils import require_admin_token

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin_token)]
)


@router.get("/protected-api")
def protected_api(session: SessionStore = Depends(require_admin_token)):
    return "Protected API Access Granted"
