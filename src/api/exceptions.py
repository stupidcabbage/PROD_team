from fastapi.responses import JSONResponse
from schemas.exceptions import BaseDBException

from main import app


@app.exception_handler(BaseDBException)
async def db_exception_handler(request, exc):
    return JSONResponse(status_code=409, content={"error": exc.details})
