from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.exceptions import BaseDBException


async def db_exception_handler(request: Request, exc: BaseDBException):
    return JSONResponse(status_code=409, content={"error": exc.details})
