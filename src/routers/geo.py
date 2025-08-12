from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.database.session import get_async_session
from src.schemas.organisation import OrganisationOut
from src.services.routers.geo import (
    get_organisations_within_radius,
    get_organisations_within_rectangle,
)

api = APIRouter(prefix="/geo", tags=["geo"])


@api.get("/organisations")
async def get_by_radius(
    lat: Annotated[
        float,
        Query(
            ge=-90,
            le=90,
        ),
    ],
    lon: Annotated[
        float,
        Query(
            ge=-180,
            le=180,
        ),
    ],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    radius: Annotated[int | None, Query(gt=0, description="Radius in meters")] = None,
) -> list[OrganisationOut]:
    return await get_organisations_within_radius(lat, lon, radius, session)


@api.get("/rectangle/organisations")
async def get_by_rectangle(
    lat: Annotated[
        float,
        Query(
            ge=-90,
            le=90,
        ),
    ],
    lon: Annotated[
        float,
        Query(
            ge=-180,
            le=180,
        ),
    ],
    width: Annotated[int | None, Query(gt=0, description="Width in meters")],
    length: Annotated[int | None, Query(gt=0, description="Length in meters")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[OrganisationOut]:
    return await get_organisations_within_rectangle(lat, lon, width, length, session)
