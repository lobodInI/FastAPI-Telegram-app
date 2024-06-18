from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from app.config import Settings


def get_database_url(config: Settings) -> str:
    username = config.postgres_user
    password = config.postgres_password
    host = config.postgres_host
    db = config.postgres_db

    return f"postgresql+asyncpg://{username}:{password}@{host}/{db}"


def create_engine(config: Settings) -> AsyncEngine:
    return create_async_engine(get_database_url(config))


def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine)
