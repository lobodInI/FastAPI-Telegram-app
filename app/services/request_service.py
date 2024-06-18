from app.db.models.models import User, Request
from app.repositories.request_repo import RequestRepository
from app.utils.exceptions import (
    RequestNotFoundException,
    AccessRequestException
)
from app.utils.telegram import send_message


class RequestService:
    def __init__(
            self,
            request_repo: RequestRepository
    ) -> None:
        self.request_repo = request_repo

    async def get_all_requests(
            self,
            limit: int,
            offset: int,
            current_user: User
    ) -> list[Request]:
        if current_user.role == "admin":
            return await self.request_repo.get_all_requests(
                limit=limit,
                offset=offset
            )

        elif current_user.role == "manager":
            return await self.request_repo.get_all_request_for_manager(
                manager_id=current_user.id
            )

        return await self.request_repo.get_all_request_for_user(
            user_id=current_user.id
        )

    async def get_request_by_id(
            self,
            request_id: str,
            current_user: User
    ) -> Request | None:
        request = await self.request_repo.get_one_request(request_id=request_id)

        if not request:
            raise RequestNotFoundException("ID", request_id)

        if (current_user.role == "user") and (current_user.id != request.owner_id):
            raise AccessRequestException("ID", request_id)

        return request

    async def create_request(
            self,
            request_data: dict,
            current_user: User
    ) -> Request | None:
        response_telegram_api = send_message(
            bot_token=request_data["bot_token"],
            chat_id=request_data["chat_id"],
            message=request_data["message"]
        )
        request_data["response"] = response_telegram_api.json()
        request_data["owner_id"] = current_user.id

        return await self.request_repo.create_request(request_data=request_data)

    async def delete_request(
            self,
            request_id: str,
            current_user: User
    ) -> dict | None:
        request = await self.request_repo.get_one_request(request_id=request_id)

        if not request:
            raise RequestNotFoundException("ID", request_id)

        if (current_user.id != request.owner_id) or (current_user.role != "admin"):
            raise AccessRequestException("ID", request_id)

        return await self.request_repo.delete_request(request_id=request_id)
