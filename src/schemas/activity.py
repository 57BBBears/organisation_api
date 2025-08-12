from __future__ import annotations
from typing import TYPE_CHECKING

from src.schemas.base import CustomBaseModel

if TYPE_CHECKING:
    from src.schemas.organisation import Organisation


class ActivityBase(CustomBaseModel):
    name: str


class ActivityIn(ActivityBase):
    parent_id: int | None = None
    children: list[ActivityIn] = []


class Activity(ActivityBase):
    id: int
    parent: Activity | None = None
    organisations: list["Organisation"] = []


class ActivityOut(ActivityBase):
    id: int
    parent_id: int | None = None
