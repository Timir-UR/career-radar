from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Vacancy, Source
from app.dedup.hashing import make_content_hash
from app.schemas.vacancy import NormalizeVacancy


async def save_vacancy(
    session: AsyncSession, source: Source, items: list[NormalizeVacancy]
) -> int:
    if not items:
        return 0
    unique: dict[str, dict] = {}
    for vitem in items:
        content_hash = make_content_hash(vitem)
        unique[content_hash] = {
            "source_id": source.id,
            "external_id": vitem.external_id,
            "title": vitem.title,
            "company": vitem.company,
            "city": vitem.city,
            "url": vitem.url,
            "salary_min": vitem.salary_min,
            "content_hash": content_hash,
        }

    stmt = (
        insert(Vacancy)
        .values(list(unique.values()))
        .on_conflict_do_nothing(index_elements=["content_hash"])
        .returning(Vacancy.id)
    )
    result = await session.execute(stmt)
    saved = len(result.all())
    return saved


async def get_source(session: AsyncSession, source_name: str) -> Source | None:
    result = await session.execute(select(Source).where(Source.name == source_name))
    return result.scalar_one_or_none()
