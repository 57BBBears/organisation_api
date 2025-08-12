from itertools import cycle
from faker import Faker
from random import randint, sample
from sqlalchemy.ext.asyncio import AsyncSession
from phonenumbers import parse, is_valid_number_for_region, NumberParseException

from src.models import Building, Activity
from src.schemas.organisation import OrganisationIn
from src.services.database.query import get_all

faker = Faker("ru_RU")


async def get_organisation_seeds(
    seed_n: int, session: AsyncSession
) -> list[OrganisationIn]:
    organisations = []
    building_iterator = cycle(await get_all(Building, session))
    activity_ids = [act.id for act in await get_all(Activity, session)]
    for _ in range(seed_n):
        organisations.append(
            OrganisationIn(
                building_id=next(building_iterator).id,
                name=faker.company(),
                phones=[get_valid_phone_number() for _ in range(randint(1, 3))],
                activities=sample(
                    activity_ids, k=randint(1, min(3, len(activity_ids)))
                ),
            )
        )

    return organisations


def get_valid_phone_number():
    while True:
        try:
            number = parse(faker.phone_number(), "RU")
            if is_valid_number_for_region(number, "RU"):
                return number
        except NumberParseException:
            continue
