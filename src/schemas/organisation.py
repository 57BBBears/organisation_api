from pydantic import BeforeValidator
from typing import Any, Annotated

from src.models import Phone as PhoneDB
from src.schemas.base import CustomBaseModel
from src.schemas.building import Building, BuildingOut
from src.schemas.activity import Activity, ActivityOut
from src.schemas.phone import Phone, RUPhoneNumber


def convert_phone_model_to_phonenumber(value: Any):
    if isinstance(value, PhoneDB):
        return value.number

    return value


class OrganisationBase(CustomBaseModel):
    name: str
    phones: list[RUPhoneNumber] = []


class OrganisationIn(OrganisationBase):
    building_id: int
    activities: list[int] = []


class Organisation(OrganisationBase):
    id: int
    building: "Building"
    phones: list[Phone] = []
    activities: list[Activity] = []


class OrganisationOut(Organisation):
    building: BuildingOut
    phones: list[
        Annotated[RUPhoneNumber, BeforeValidator(convert_phone_model_to_phonenumber)]
    ] = []
    activities: list[ActivityOut] = []
