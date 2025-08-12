from typing import TypeVar, Sequence

from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.models import Organisation, Base


def get_organisation_query() -> Select:
    return select(Organisation).options(
        joinedload(Organisation.building),
        selectinload(Organisation.phones),
        selectinload(Organisation.activities),
    )


T = TypeVar("T", bound=Base)


def get_count_query(model: type[T]) -> Select:
    return select(func.count()).select_from(model)


async def get_all(model: type[T], session: AsyncSession) -> Sequence[T]:
    return (await session.scalars(select(model))).all()
