from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_config import get_current_user
from app.dependencies.db_depends import get_session
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.schemas import user_schemas
from app.db.models.models import User

router = APIRouter()


async def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    user_repository = UserRepository(session=session)

    return UserService(user_repository=user_repository)


@router.get(
    "/user/all/",
    response_model=list[user_schemas.UsersList]
)
async def get_all_users(
        user_service: UserService = Depends(get_user_service),
        limit: int = 100,
        offset: int = 0
):
    return await user_service.get_all_users(limit=limit, offset=offset)


@router.get(
    "/user/{user_id}",
    response_model=user_schemas.UserDetail
)
async def get_user(
        user_id: str,
        user_service: UserService = Depends(get_user_service)
) -> Optional[User]:
    return await user_service.get_user_by_id(user_id=user_id)


@router.post(
    "/user/create/",
    response_model=user_schemas.UserDetail
)
async def create_user(
        user: user_schemas.SignUpUser,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.sign_up_user(user_data=user.model_dump())


@router.put(
    "/user/{user_id}/",
    response_model=user_schemas.UserDetail
)
async def update_user(
        user_id: str,
        user: user_schemas.UserUpdate,
        user_service: UserService = Depends(get_user_service),
        user_by_token: User = Depends(get_current_user)
):
    return await user_service.update_user(
        user_id=user_id,
        user_data=user.model_dump(),
        user_by_token=user_by_token
    )


@router.delete("/user/{user_id}/")
async def delete_user(
        user_id: str,
        user_service: UserService = Depends(get_user_service),
        user_by_token: User = Depends(get_current_user)
) -> dict:
    return await user_service.delete_user(
        user_id=user_id,
        user_by_token=user_by_token
    )


@router.get("/me/", response_model=user_schemas.UserDetail)
async def get_info_about_me(
        user: User = Depends(get_current_user)
) -> User:
    return user
