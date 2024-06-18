from typing import Type

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import User
from app.repositories.base_repo import BaseRepository
from app.schemas import user_schemas


class UserRepository(BaseRepository[User]):

    def __init__(
            self,
            session: AsyncSession,
            model: Type[User] = User
    ) -> None:
        super().__init__(session, model)

    async def find_all_user(
            self,
            limit: int = 100,
            offset: int = 0
    ) -> list[user_schemas.UsersList]:
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        users = result.scalars().all()

        return users

    async def find_one_user(
            self,
            user_id: str
    ) -> user_schemas.UserDetail | None:
        query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()

        return user

    async def check_user_by_username(self, username: str) -> bool:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        user = result.scalars().first()

        return bool(user)

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()

        return user

    async def create_user(self, user: dict[str, str]) -> User | None:
        user_model = self.model(**user)
        self.session.add(user_model)

        await self.session.commit()
        await self.session.refresh(user_model)

        return user_model

    async def update_user(
            self,
            user_id: str,
            user_data: dict[str, str]
    ) -> user_schemas.UserDetail | None:
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**user_data).returning(self.model)
        )
        result = await self.session.execute(query)
        user = result.scalars().one()

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete_user(self, user_id: str) -> dict:
        query = delete(self.model).where(self.model.id == user_id)
        await self.session.execute(query)
        await self.session.commit()

        return {"detail": f"User with ID: {user_id} has been deleted!"}
