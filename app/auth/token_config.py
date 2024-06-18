import jwt

from jwt.exceptions import PyJWTError

from app.config import settings
from app.utils.exceptions import UserUnauthorizedException


class Token:
    def __init__(self, token) -> None:
        self.token = token
        self.config = settings


class CustomToken(Token):

    def get_payload(self) -> dict | None:
        try:
            payload = jwt.decode(
                self.token.credentials,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            return payload

        except PyJWTError as error:
            raise UserUnauthorizedException(
                message=str(error)
            )
