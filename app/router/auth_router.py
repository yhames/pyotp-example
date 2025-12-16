import pyotp
from fastapi import APIRouter, Depends
from fastapi import Header, HTTPException

from app.security import get_totp

router = APIRouter(prefix="/auth")


@router.post("/verify-otp")
def verify_otp(x_otp: str = Header(..., description="6-digit TOTP code"), totp: pyotp.TOTP = Depends(get_totp)):
    if not totp.verify(x_otp, valid_window=1):
        raise HTTPException(status_code=403, detail="Invalid OTP")
    return {"status": "ok"}
