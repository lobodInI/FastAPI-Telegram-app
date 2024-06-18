from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
            self,
            session: AsyncSession,
            model: Type[ModelType]
    ) -> None:
        self.session = session
        self.model = model
