from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


def require_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials
