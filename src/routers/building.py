from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.organisation import OrganisationOut
from src.services.database.session import get_async_session
from src.services.routers.building import get_organisations_by_building_id

api = APIRouter(prefix="/buildings", tags=["buildings"])


@api.get("/{building_id}/organisations")
async def get_organisations(
    building_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Sequence[OrganisationOut]:
    # TODO raise error if building_id is not found ?
    return await get_organisations_by_building_id(building_id, session)
