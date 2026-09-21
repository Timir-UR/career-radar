from sqlalchemy import select, func
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.vacancy import VacancyRead
from app.db.models import Vacancy
from app.db.session import get_async_session
from app.core.constants import SEARCH_CONFIG
router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("", response_model=list[VacancyRead])
async def get_vacancies(
    city: str | None = Query(None),
    company: str | None = Query(None),
    salary_min: int | None = Query(None, ge=0),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = select(Vacancy)

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

    results = await session.execute(stmt)
    return results.scalars().all()

@router.get("/search", response_model=list[VacancyRead])
async def get_vacancies_search(
    session: AsyncSession = Depends(get_async_session),
    q: str = Query(min_length=2),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = select(Vacancy)
    stmt = stmt.where(Vacancy.search_vector.op("@@")(func.websearch_to_tsquery(SEARCH_CONFIG, q)))
    stmt = (
        stmt
        .order_by(Vacancy.first_seen_at.desc(), Vacancy.id.desc())
        .limit(limit)
        .offset(offset)
    )
    results = await session.execute(stmt)
    return results.scalars().all()