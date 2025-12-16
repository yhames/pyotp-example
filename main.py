from app import create_app
from app.config import get_settings

app = create_app()

settings = get_settings()

def run():
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    run()
