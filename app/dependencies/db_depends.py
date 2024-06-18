from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.postgres_config import (
    create_async_sessionmaker,
    create_engine
)


async def get_session() -> AsyncSession:
    engine = create_engine(settings)
    async_session = create_async_sessionmaker(engine)
    async with async_session() as session:
        yield session
