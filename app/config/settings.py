from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str
    host: str
    port: int
    totp_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def get_settings():
    return settings
