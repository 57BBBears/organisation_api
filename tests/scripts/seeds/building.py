from faker import Faker

from src.schemas.building import BuildingIn


def get_building_seeds(seed_n: int) -> list[BuildingIn]:
    faker = Faker("ru_RU")
    buildings = []
    for _ in range(seed_n):
        location = faker.local_latlng("RU", coords_only=True)
        buildings.append(
            BuildingIn(address=faker.address(), coordinates=(location[0], location[1]))
        )

    return buildings
