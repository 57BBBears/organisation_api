from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.building import BuildingIn
from src.models import Building


async def seed_building(buildings: list[BuildingIn], session: AsyncSession):
    seeded = (await session.execute(select((exists().select_from(Building))))).scalar()

    if seeded:
        print("Buildings exist")
        return

    for building in buildings:
        model = Building(**building.model_dump())
        session.add(model)

    await session.commit()
    print("Buildings seeded")
