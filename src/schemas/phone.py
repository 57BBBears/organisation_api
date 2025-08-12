from typing import Annotated
from pydantic_extra_types.phone_numbers import PhoneNumberValidator, PhoneNumber

from src.schemas.base import CustomBaseModel

RUPhoneNumber = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(
        supported_regions=["RU"], default_region="RU", number_format="E164"
    ),
]


class PhoneBase(CustomBaseModel):
    organisation_id: int
    number: RUPhoneNumber


class Phone(PhoneBase):
    id: int
