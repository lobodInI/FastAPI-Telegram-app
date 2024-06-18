from app.auth.auth_config import get_access_token
from app.repositories.user_repo import UserRepository
from app.schemas.user_schemas import SignInUser
from app.utils.exceptions import UserUnauthorizedException
from app.utils.password_utils import verify_password


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository
    ) -> None:
        self.user_repository = user_repository

    async def get_access_jwt_token(
            self,
            signin_body: SignInUser
    ) -> dict[str, str] | None:
        user = await self.user_repository.get_user_by_email(signin_body.email)

        if not user:
            raise UserUnauthorizedException(
                message="Invalid email or password",
            )
        if not verify_password(signin_body.password, user.password):
            raise UserUnauthorizedException(
                message="Invalid email or password",
            )

        access_token = get_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
