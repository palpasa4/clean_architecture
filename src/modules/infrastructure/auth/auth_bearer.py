from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from httpx import request
import jwt
from src.modules.infrastructure.logging.logconfig import logger
from src.modules.infrastructure.persistence.settings import DefaultSettings
from .auth_handler import decode_jwt
from typing import Optional


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JWTBearer, self
        ).__call__(request)

        settings: DefaultSettings = request.app.state.settings.default
        if credentials:
            if not credentials.scheme == "Bearer":
                logger.info(
                    "Authentication failed: Invalid authentication scheme (HTTP 403)."
                )
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials, settings):
                logger.info(
                    "Authentication failed: Invalid or expired token (HTTP 403)."
                )
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            token = credentials.credentials
            decoded_token = jwt.decode(
                token,
                settings.secret.get_secret_value(),
                algorithms=[settings.algorithm],
            )
            username = decoded_token.get("user_id")
            return username
        else:
            logger.info("Authentication failed: Invalid authorization code (HTTP 403).")
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, settings: DefaultSettings) -> bool:
        # breakpoint()
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken, settings)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
