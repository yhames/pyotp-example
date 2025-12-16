from fastapi import APIRouter, Depends, Request
from fastapi import Header, HTTPException

from app.config import get_settings
from app.dto import TokenResponse
from app.security import get_otp_helper, create_session
from app.security.session_store import get_session, revoke_session
from app.security.totp_helper import OtpHelper

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

settings = get_settings()


@router.post("/login/otp", response_model=TokenResponse)
def login_otp(
        request: Request,
        x_otp: str = Header(..., description="6-digit TOTP code"),
        otp_helper: OtpHelper = Depends(get_otp_helper),
) -> TokenResponse:
    client_ip = request.client.host

    # 1. IP 차단 여부 확인
    if otp_helper.is_blocked(client_ip):
        raise HTTPException(status_code=429, detail="Too many OTP attempts")

    # 2. OTP 재사용 방지
    if otp_helper.is_used_otp(client_ip, x_otp):
        raise HTTPException(status_code=429, detail="OTP already used")

    # 3. OTP 검증
    if not otp_helper.verify_otp(x_otp):
        raise HTTPException(status_code=403, detail="Invalid OTP")

    # 4. 성공 처리
    otp_helper.mark_otp_as_used(client_ip, x_otp)
    otp_helper.reset_failures(client_ip)

    # 5. 세션 생성 및 토큰 반환
    session_token = create_session(client_ip)
    expires_in = settings.session_absolute_timeout
    return TokenResponse(access_token=session_token, expires_in=expires_in)


@router.post("/logout")
def logout(
        request: Request,
        x_token: str = Header(..., description="Session token to revoke"),
):
    client_ip = request.client.host
    session_id = x_token

    session = get_session(session_id, client_ip)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    revoke_session(session_id)
    return {"detail": "Logged out successfully"}
