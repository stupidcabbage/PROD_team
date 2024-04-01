from typing import Literal

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from config import jwt_config


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Incorrect authorization schema.")
            verify_jwt_status = await self.verify_jwt(credentials.credentials)

            if not verify_jwt_status:
                raise HTTPException(
                    status_code=401, detail="Invalid or expired token.")
            return verify_jwt_status
        else:
            raise HTTPException(status_code=401,
                                detail="Invalid token authorization.")

    async def verify_jwt(self, jwtoken: str) -> Literal[False] | int:
        try:
            payload = await decodeJWT(jwtoken)
        except Exception:
            return False
        if payload:
            return payload.get("user_id")
        return False


async def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, jwt_config.secret_key,
                                   algorithms=["HS256"])
        return decoded_token
    except Exception:
        return {}
