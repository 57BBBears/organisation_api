from typing import Annotated

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import NoResultFound

from src.services.database.session import get_async_session
from src.schemas.organisation import OrganisationOut
from src.services.routers.organisation import (
    get_organisation_by_id,
    get_organisation_by_name,
    get_all,
)


api = APIRouter(prefix="/organisations", tags=["organisations"])


@api.get("/")
async def get_organisations(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    name: Annotated[str | None, Query(description="Search by name")] = None,
) -> list[OrganisationOut]:
    if name:
        return await get_organisation_by_name(name, session)

    return await get_all(session)


@api.get("/{organisation_id}")
async def get_organisation(
    organisation_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> OrganisationOut:
    try:
        return await get_organisation_by_id(organisation_id, session)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )
