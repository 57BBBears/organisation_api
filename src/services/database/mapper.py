from sqlalchemy import Row

from src.schemas.organisation import OrganisationOut
from src.schemas.building import Building


def row_to_organisation_out(row: Row) -> OrganisationOut:
    return OrganisationOut(
        **row[0].as_dict(), building=Building(**row[1].as_dict()), phones=row[2]
    )
