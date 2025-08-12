from typing import Sequence
from sqlalchemy import func, select, Subquery
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from src.models import Organisation, Building
from src.services.database.query import get_organisation_query


async def get_organisations_within_radius(
    lat: float, lon: float, radius: int | None, session: AsyncSession
) -> Sequence[Organisation]:
    subquery = get_building_ids_within_radius_query(
        lat, lon, radius or config.min_radius
    )

    query = get_organisation_query().join(
        subquery, Organisation.building_id == subquery.c.id
    )

    return (await session.scalars(query)).all()


async def get_organisations_within_rectangle(
    lat: float, lon: float, width: int, length: int, session: AsyncSession
) -> Sequence[Organisation]:
    subquery = get_building_ids_within_rectangle_query(lat, lon, width, length)

    query = get_organisation_query().join(
        subquery, Organisation.building_id == subquery.c.id
    )

    return (await session.scalars(query)).all()


def get_building_ids_within_radius_query(
    lat: float, lon: float, radius: int
) -> Subquery:
    point = func.ST_GeogFromText(f"POINT({lon} {lat})")

    return (
        select(Building.id)
        .where(func.ST_Distance(Building.coordinates, point) <= radius)
        .subquery()
    )


def get_building_ids_within_rectangle_query(
    lat: float, lon: float, width: int, length: int
) -> Subquery:
    center_point = func.ST_SetSRID(
        func.ST_MakePoint(lon, lat),
        4326,  # WGS84
    )

    center_mercator = func.ST_Transform(center_point, 3857)

    half_width_m = width / 2
    half_height_m = length / 2

    rectangle_mercator = func.ST_MakeEnvelope(
        func.ST_X(center_mercator) - half_width_m,
        func.ST_Y(center_mercator) - half_height_m,
        func.ST_X(center_mercator) + half_width_m,
        func.ST_Y(center_mercator) + half_height_m,
        3857,
    )

    rectangle_wgs84 = func.ST_Transform(rectangle_mercator, 4326)

    return (
        select(Building.id)
        .where(func.ST_Within(Building.coordinates, rectangle_wgs84))
        .subquery()
    )
