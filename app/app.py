from fastapi import FastAPI

from app.router import admin_router, auth_router


def create_app():
    app = FastAPI()

    app.include_router(admin_router)
    app.include_router(auth_router)

    return app
