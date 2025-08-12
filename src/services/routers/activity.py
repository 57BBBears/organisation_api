from typing import Sequence
from sqlalchemy import select, Subquery
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Organisation, OrganisationActivity, Activity
from src.services.database.query import get_organisation_query


async def get_organisations_by_activity_id(
    activity_id: int, session: AsyncSession, depth: int = 1
) -> Sequence[Organisation]:
    if depth == 1:
        query = (
            get_organisation_query()
            .join(OrganisationActivity)
            .join(Activity)
            .where(Activity.id == activity_id)
            .order_by(Organisation.id)
        )
    else:
        ids_subquery = get_activity_ids_subquery(activity_id, depth)
        query = (
            get_organisation_query()
            .distinct()
            .join(OrganisationActivity)
            .join(ids_subquery, OrganisationActivity.activity_id == ids_subquery.c.id)
        )

    return (await session.scalars(query)).all()


def get_activity_ids_subquery(root_id: int, depth: int) -> Subquery:
    return (
        select(Activity.id)
        .where(Activity.id == root_id)
        .options(selectinload(Activity.children, recursion_depth=depth))
        .subquery()
    )
