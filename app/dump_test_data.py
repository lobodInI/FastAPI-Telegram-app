import json
import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.models.models import User, Request
from app.db.postgres_config import get_database_url
from app.utils.password_utils import hash_password

db_url = get_database_url(config=settings)

engine = create_async_engine(db_url, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def load_data():
    async with AsyncSessionLocal() as session:
        with open("app/test_data.json", "r") as file:
            data = json.load(file)

        for user in data["users"]:
            new_user = User(
                id=UUID(user["id"]),
                username=user["username"],
                email=user["email"],
                password=hash_password(user["password"]),
                role=user["role"],
                manager_id=user["manager_id"]
            )
            session.add(new_user)

        for request in data["requests"]:
            new_request = Request(
                id=UUID(request["id"]),
                bot_token=request["bot_token"],
                chat_id=request["chat_id"],
                message=request["message"],
                response=request["response"],
                owner_id=request["owner_id"]
            )
            session.add(new_request)

        await session.commit()


if __name__ == '__main__':
    asyncio.run(load_data())
