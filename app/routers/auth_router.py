from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db_depends import get_session
from app.repositories.user_repo import UserRepository
from app.schemas.token_schemas import BaseToken
from app.schemas.user_schemas import SignInUser
from app.services.auth_service import AuthService

router = APIRouter()


async def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    user_repository = UserRepository(session=session)
    return AuthService(user_repository=user_repository)


@router.post("/auth/signin/", response_model=BaseToken)
async def sign_in(
        signin_body: SignInUser = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_access_jwt_token(signin_body)
