from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SEARCH_CONFIG
from app.db.models import Vacancy


async def list_vacancies(
        session: AsyncSession,
        *,
        q: str | None = None,
        city: str | None = None,
        company: str | None = None,
        salary_min: int | None = None,
        limit: int = 20,
        offset: int = 0,
) -> list[Vacancy]:
    """Вакансии с фильтрами и полнотекстовым поиском, новые сверху."""
    stmt = select(Vacancy)

    if q is not None:
        stmt = stmt.where(
            Vacancy.search_vector.op("@@")(func.websearch_to_tsquery(SEARCH_CONFIG, q))
        )
    if city is not None:
        stmt = stmt.where(Vacancy.city.ilike(f"%{city}%"))
    if company is not None:
        stmt = stmt.where(Vacancy.company.ilike(f"%{company}%"))
    if salary_min is not None:
        stmt = stmt.where(Vacancy.salary_min >= salary_min)

    stmt = (
        stmt
        .order_by(Vacancy.first_seen_at.desc(), Vacancy.id.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(stmt)
    return list(result.scalars().all())




