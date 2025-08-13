from typing import TYPE_CHECKING, Any, Annotated

from shapely import from_wkb
from geoalchemy2 import WKBElement
from pydantic import field_serializer, BeforeValidator
from pydantic_extra_types.coordinate import Coordinate
from src.schemas.base import CustomBaseModel

if TYPE_CHECKING:
    from src.schemas.organisation import Organisation


def convert_wkb_to_coordinate(value: Any):
    if isinstance(value, WKBElement):
        # Convert WKBElement to shapely geometry
        shapely_geom = from_wkb(bytes(value.data))
        # Extract coordinates (point example)
        if shapely_geom.geom_type == "Point":
            return Coordinate(longitude=shapely_geom.x, latitude=shapely_geom.y)

    return value


class BuildingBase(CustomBaseModel):
    address: str
    coordinates: Annotated[Coordinate, BeforeValidator(convert_wkb_to_coordinate)]

    @field_serializer("coordinates", when_used="unless-none")
    def convert_coordinates(self, coordinate: Coordinate, _info):
        if _info.mode == "python":
            # WKT
            return f"Point({coordinate.longitude} {coordinate.latitude})"

        return coordinate


class BuildingIn(BuildingBase): ...


class Building(BuildingBase):
    id: int
    organisations: list["Organisation"] = []


class BuildingOut(BuildingBase):
    id: int
