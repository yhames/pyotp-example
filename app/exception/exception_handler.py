from fastapi import status, Request
from fastapi.responses import JSONResponse

from app.dto import ErrorResponse
from main import app


@app.exception_handler(ErrorResponse)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            message=str(exc)
        ).model_dump()
    )
