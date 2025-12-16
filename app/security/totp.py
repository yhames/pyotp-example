import pyotp
from fastapi.params import Depends

from app.config.settings import Settings, get_settings


def get_totp(config: Settings = Depends(get_settings)) -> pyotp.TOTP:
    return pyotp.TOTP(config.totp_secret)
