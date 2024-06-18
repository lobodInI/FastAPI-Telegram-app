from app.db.models.models import User
from app.repositories.user_repo import UserRepository
from app.schemas import user_schemas
from app.utils.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserUnauthorizedException,
)
from app.utils.password_utils import hash_password


class UserService:
    def __init__(
            self,
            user_repository: UserRepository
    ) -> None:
        self.user_repository = user_repository

    async def get_all_users(
            self,
            limit: int,
            offset: int
    ) -> list[user_schemas.UsersList]:
        return await self.user_repository.find_all_user(
            limit=limit,
            offset=offset
        )

    async def get_user_by_id(
            self,
            user_id: str
    ) -> user_schemas.UserDetail | None:
        user = await self.user_repository.find_one_user(user_id=user_id)

        if not user:
            raise UserNotFoundException("ID", user_id)

        return user

    async def sign_up_user(
            self,
            user_data: dict
    ) -> user_schemas.UserDetail | None:
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")

        username_db = await (self.user_repository.
                             check_user_by_username(username=username))
        if username_db:
            raise UserAlreadyExistsException("username", username)

        email_db = await (self.user_repository.
                          get_user_by_email(email=email))
        if email_db:
            raise UserAlreadyExistsException("email", email)

        password_hash = hash_password(password)
        user_data["password"] = password_hash

        return await self.user_repository.create_user(user=user_data)

    async def update_user(
            self,
            user_id: str,
            user_data: dict,
            user_by_token: User
    ) -> user_schemas.UserDetail | None:
        user_by_id = await self.user_repository.find_one_user(user_id=user_id)
        if not user_by_id:
            raise UserNotFoundException("ID", user_id)

        # checking whether the user id is the same
        # as the user id from the jwt token
        if user_by_id.id != user_by_token.id:
            raise UserUnauthorizedException(
                message="User can update only his profile!",
            )

        username = user_data.get("username")
        if username:
            username_db = await (self.user_repository.
                                 check_user_by_username(username=username))
            if username_db:
                raise UserAlreadyExistsException("username", username)
        else:
            user_data["username"] = user_by_id.username

        password = user_data.get("password")
        if password:
            password_hash = hash_password(password)
            user_data["password"] = password_hash
        else:
            user_data["password"] = user_by_id.password

        return await self.user_repository.update_user(
            user_id=user_id,
            user_data=user_data
        )

    async def delete_user(
            self,
            user_id: str,
            user_by_token: User
    ) -> dict | None:
        user = await self.user_repository.find_one_user(user_id=user_id)
        if not user:
            raise UserNotFoundException("ID", user_id)

        if user.id != user_by_token.id:
            raise UserUnauthorizedException(
                message="User can delete only his profile!",
            )

        return await self.user_repository.delete_user(user_id=user_id)
