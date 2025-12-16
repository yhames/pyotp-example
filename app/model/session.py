from pydantic import BaseModel


class SessionStore(BaseModel):
    ip: str
    created_at: float
    last_access: float
