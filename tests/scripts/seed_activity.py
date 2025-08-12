from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.activity import ActivityIn
from src.models import Activity


async def seed_activity(activities: list[ActivityIn], session: AsyncSession):
    seeded = (await session.execute(select((exists().select_from(Activity))))).scalar()

    if seeded:
        print("Activities exist")
        return

    for root_activity in activities:
        root_model = Activity(name=root_activity.name)
        session.add(root_model)
        await session.flush()

        async def create_children(parent_id: int, children):
            for child in children:
                child_model = Activity(name=child.name, parent_id=parent_id)
                session.add(child_model)
                await session.flush()

                if child.children:
                    await create_children(child_model.id, child.children)

        if root_activity.children:
            await create_children(root_model.id, root_activity.children)

    await session.commit()
    print("Activities seeded")
