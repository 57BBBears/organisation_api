from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.organisation import OrganisationOut
from src.services.database.session import get_async_session
from src.services.routers.activity import get_organisations_by_activity_id

api = APIRouter(prefix="/activities", tags=["activities"])


@api.get("/{activity_id}/organisations")
async def get_organisations(
    activity_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    depth: Annotated[int, Query(ge=1, le=3)] = 1,
) -> Sequence[OrganisationOut]:
    return await get_organisations_by_activity_id(activity_id, session, depth)
