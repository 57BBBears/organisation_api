import asyncio

from src.config import config
from src.models import Building, Organisation, Activity
from src.services.database.session import Session
from src.services.database.query import get_count_query
from tests.scripts.seed_building import seed_building
from tests.scripts.seed_activity import seed_activity
from tests.scripts.seed_organisation import seed_organisation
from tests.scripts.seeds.activity import get_activity_seeds
from tests.scripts.seeds.building import get_building_seeds
from tests.scripts.seeds.organisation import get_organisation_seeds


async def main():
    async with Session() as session:
        await seed_building(get_building_seeds(config.seed.building_num), session)
        await seed_activity(get_activity_seeds(), session)
        await seed_organisation(
            await get_organisation_seeds(config.seed.organisation_num, session), session
        )

        building_count = (await session.execute(get_count_query(Building))).scalar()
        organisation_count = (
            await session.execute(get_count_query(Organisation))
        ).scalar()
        activity_count = (await session.execute(get_count_query(Activity))).scalar()

        print("\nSeeding completed:")
        print(f"- Buildings: {building_count}")
        print(f"- Organisations: {organisation_count}")
        print(f"- Activities: {activity_count}")


if __name__ == "__main__":
    asyncio.run(main())
