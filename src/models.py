from sqlalchemy import MetaData, String, ForeignKey, UniqueConstraint, inspect, Index
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
    backref,
)
from sqlalchemy_utils import PhoneNumberType
from geoalchemy2 import Geometry, WKBElement
from phonenumbers import PhoneNumber


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base:
    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


Base = declarative_base(cls=Base, metadata=metadata)


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="cascade")
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    children: Mapped[list["Activity"]] = relationship(
        backref=backref("parent", remote_side=[id], passive_deletes=True)
    )
    organisations: Mapped[list["Organisation"]] = relationship(
        back_populates="activities",
        secondary="organisations_activities",
        passive_deletes=True,
    )


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    coordinates: Mapped[str | WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=False
    )

    organisations: Mapped[list["Organisation"]] = relationship(
        "Organisation", back_populates="building", passive_deletes=True
    )


class Phone(Base):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.id", ondelete="cascade"), nullable=False
    )
    number: Mapped[PhoneNumber] = mapped_column(
        PhoneNumberType(region="RU", max_length=12), nullable=False
    )

    organisation: Mapped["Organisation"] = relationship(
        "Organisation", back_populates="phones"
    )

    UniqueConstraint(organisation_id, number, name="phones_organisation_id_number_key")


class Organisation(Base):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(
        ForeignKey(Building.id, ondelete="cascade"), nullable=False
    )

    building: Mapped[Building] = relationship(
        Building, foreign_keys=[building_id], back_populates="organisations"
    )
    activities: Mapped[list[Activity]] = relationship(
        back_populates="organisations",
        secondary="organisations_activities",
        passive_deletes=True,
    )
    phones: Mapped[list[Phone]] = relationship(
        Phone, back_populates="organisation", passive_deletes=True
    )

    __table_args__ = (
        Index(
            "organisations_name_idx",
            "name",
            postgresql_ops={"name": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
    )


class OrganisationActivity(Base):
    """A many-to-many table."""

    __tablename__ = "organisations_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey(Organisation.id, ondelete="cascade"), nullable=False
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey(Activity.id, ondelete="cascade"), nullable=False
    )

    UniqueConstraint(
        organisation_id,
        activity_id,
        name="organisations_activities_organisation_id_activity_id_key",
    )
