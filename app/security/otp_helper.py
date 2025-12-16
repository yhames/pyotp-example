import pyotp
from cachetools import TTLCache

from app.config import get_settings

# OTP 재사용 방지
_used_otps = TTLCache(maxsize=100, ttl=30)

# IP 차단
_blocked_ips = TTLCache(maxsize=1000, ttl=300)

# 실패한 시도 기록
_failed_attempts = TTLCache(maxsize=1000, ttl=300)


class OtpHelper:
    def __init__(self):
        settings = get_settings()
        self.max_attempts = settings.otp_max_attempts
        self.totp = pyotp.TOTP(settings.totp_secret)

    # ---------- brute force ----------

    @staticmethod
    def is_blocked(ip: str) -> bool:
        return ip in _blocked_ips

    @staticmethod
    def reset_failures(ip: str):
        _failed_attempts.pop(ip, None)
        _blocked_ips.pop(ip, None)

    def record_failure(self, ip: str):
        _failed_attempts[ip] = _failed_attempts.get(ip, 0) + 1
        if _failed_attempts[ip] >= self.max_attempts:
            _blocked_ips[ip] = True
            _failed_attempts.pop(ip, None)

    # ---------- OTP ----------

    def verify_otp(self, otp: str) -> bool:
        return self.totp.verify(otp, valid_window=1)

    def is_used_otp(self, ip: str, otp: str) -> bool:
        key = self.get_used_otp_key(ip, otp)
        return key in _used_otps

    def mark_otp_as_used(self, ip: str, otp: str):
        key = self.get_used_otp_key(ip, otp)
        _used_otps[key] = True

    @staticmethod
    def get_used_otp_key(ip: str, otp: str) -> str:
        return f"{ip}:{otp}"


_otp_helper = OtpHelper()


def get_otp_helper() -> OtpHelper:
    return _otp_helper
