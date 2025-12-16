from fastapi import APIRouter, Depends

from app.security.token import require_admin_token

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin_token)]
)


@router.get("/protected-api")
def protected_api(token: str = Depends(require_admin_token)):
    return "Protected API Access Granted"
