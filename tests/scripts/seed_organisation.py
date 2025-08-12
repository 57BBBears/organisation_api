from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.organisation import OrganisationIn
from src.models import Organisation, OrganisationActivity, Phone


async def seed_organisation(organisations: list[OrganisationIn], session: AsyncSession):
    seeded = (
        await session.execute(select((exists().select_from(Organisation))))
    ).scalar()

    if seeded:
        print("Organisations exist")
        return

    for org in organisations:
        org_model = Organisation(**org.model_dump(exclude={"activities", "phones"}))
        session.add(org_model)
        await session.flush()

        # seed phones
        for number in org.phones:
            phone_model = Phone(organisation_id=org_model.id, number=number)
            session.add(phone_model)

        # seed many-to-many table
        for act_id in org.activities:
            org_act_model = OrganisationActivity(
                organisation_id=org_model.id, activity_id=act_id
            )
            session.add(org_act_model)

    await session.commit()
    print("Organisations seeded")
