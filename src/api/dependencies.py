from typing import Annotated

from fastapi import Depends

from api.auth import JWTBearer

JWTAuth = Annotated[int, Depends(JWTBearer())]
