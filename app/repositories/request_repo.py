from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Request, User
from app.repositories.base_repo import BaseRepository


class RequestRepository(BaseRepository[Request]):
    def __init__(
            self,
            session: AsyncSession,
            model: Type[Request] = Request
    ) -> None:
        super().__init__(session, model)

    async def get_all_requests(
            self,
            limit: int = 100,
            offset: int = 0
    ) -> list[Request]:
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        requests = result.scalars().all()

        return requests

    async def get_one_request(self, request_id: str) -> Request:
        query = select(self.model).where(self.model.id == request_id)
        result = await self.session.execute(query)
        request = result.scalars().first()

        return request

    async def get_all_request_for_user(self, user_id: int) -> list[Request]:
        query = select(self.model).where(self.model.owner_id == user_id)
        result = await self.session.execute(query)
        requests = result.scalars().all()

        return requests

    async def get_all_request_for_manager(self, manager_id: str) -> list[Request]:
        query = (
            select(self.model)
            .join(User, self.model.owner_id == User.id)
            .where(User.manager_id == manager_id)
        )
        result = await self.session.execute(query)
        requests = result.scalars().all()

        return requests

    async def create_request(self, request_data: dict) -> Request:
        request_model = self.model(**request_data)
        self.session.add(request_model)

        await self.session.commit()
        await self.session.refresh(request_model)

        return request_model

    async def delete_request(self, request_id: str) -> dict:
        query = delete(self.model).where(self.model.id == request_id)
        await self.session.execute(query)
        await self.session.commit()

        return {"detail": f"Request with ID: {request_id} has been deleted!"}
