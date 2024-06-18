from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_config import get_current_user
from app.db.models.models import User
from app.dependencies.db_depends import get_session
from app.repositories.request_repo import RequestRepository
from app.services.request_service import RequestService
from app.schemas.request_schemas import RequestDetail, RequestCreate

router = APIRouter()


async def get_request_service(
        session: AsyncSession = Depends(get_session)
) -> RequestService:
    request_repo = RequestRepository(session=session)

    return RequestService(request_repo=request_repo)


@router.get("/request/all/", response_model=list[RequestDetail])
async def get_all_requests(
        request_service: RequestService = Depends(get_request_service),
        current_user: User = Depends(get_current_user),
        limit: int = 100,
        offset: int = 0
):
    return await request_service.get_all_requests(
        limit=limit,
        offset=offset,
        current_user=current_user
    )


@router.get("/request/{request_id}/", response_model=RequestDetail)
async def get_one_request(
        request_id: str,
        request_service: RequestService = Depends(get_request_service),
        current_user: User = Depends(get_current_user),
):
    return await request_service.get_request_by_id(
        request_id=request_id,
        current_user=current_user
    )


@router.post("/request/create/", response_model=RequestDetail)
async def create_request(
        request_data: RequestCreate,
        request_service: RequestService = Depends(get_request_service),
        current_user: User = Depends(get_current_user),
):
    return await request_service.create_request(
        request_data=request_data.model_dump(),
        current_user=current_user
    )


@router.delete("/request/delete/")
async def delete_request(
        request_id: str,
        request_service: RequestService = Depends(get_request_service),
        current_user: User = Depends(get_current_user),
):
    return await request_service.delete_request(
        request_id=request_id,
        current_user=current_user
    )
