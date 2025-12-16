from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str
    host: str = "127.0.0.1"
    port: int = 8080
    totp_secret: str
    session_ttl: int = 7200  # seconds
    session_absolute_timeout: int = 3600  # seconds
    session_idle_timeout: int = 1800  # seconds
    otp_max_attempts: int = 5  # maximum failed OTP attempts before blocking

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def get_settings():
    return settings
