from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Organisation
from src.services.database.query import get_organisation_query


async def get_organisation_by_id(
    organisations_id: int, session: AsyncSession
) -> Organisation:
    query = get_organisation_query().where(Organisation.id == organisations_id)

    return (await session.execute(query)).scalar_one()


async def get_organisation_by_name(
    name: str, session: AsyncSession
) -> Sequence[Organisation]:
    query = get_organisation_query().where(Organisation.name.ilike(f"%{name}%"))

    return (await session.scalars(query)).all()


async def get_all(session: AsyncSession) -> Sequence[Organisation]:
    return (await session.scalars(get_organisation_query())).all()
