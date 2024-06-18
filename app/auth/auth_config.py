import jwt

from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.token_config import CustomToken
from app.db.models.models import User
from app.dependencies.db_depends import get_session
from app.repositories.user_repo import UserRepository
from app.config import settings
from app.utils.exceptions import (
    UserNotFoundException,
    UserUnauthorizedException,
)

token_auth_scheme = HTTPBearer()


def get_email(payload: dict[str, str]) -> str:
    email = payload.get("email")

    if email is None:
        email = payload.get("sub")

        if email is None:
            raise UserUnauthorizedException(
                message="Email is missing from the "
                        "payload data of the token!"
            )

    return email


async def get_user_repository(
        session: AsyncSession = Depends(get_session)
) -> UserRepository:
    return UserRepository(session=session)


async def get_current_user(
        token: str = Depends(token_auth_scheme),
        user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    payload = CustomToken(token).get_payload()

    email = get_email(payload)

    user = await user_repo.get_user_by_email(email=email)

    if user is None:
        raise UserNotFoundException("email", email)

    return user


def get_access_token(data: dict[str, str]) -> str:
    expire_time = datetime.now() + timedelta(
        minutes=settings.token_expire_minutes
    )
    data.update({"exp": expire_time})

    token = jwt.encode(
        data,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return token
