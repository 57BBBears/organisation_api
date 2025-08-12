from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.models import Organisation
from src.services.database.query import get_organisation_query


async def get_organisations_by_building_id(
    building_id: int, session: AsyncSession
) -> Sequence[Organisation]:
    query = (
        get_organisation_query()
        .where(Organisation.building_id == building_id)
        .order_by(Organisation.id)
    )

    return (await session.scalars(query)).all()
