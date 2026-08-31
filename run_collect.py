import asyncio

from pydantic import ValidationError

from app.collectors.remotive import fetch_remotive_jobs
from app.db.session import async_session_maker
from app.db.storage import save_vacancy
from app.normalizers.remotive import normalize_remotive


async def collect() -> None:
    raw_jobs = await fetch_remotive_jobs()
    print(f"Получено с Remotive: {len(raw_jobs)}")

    normalized = []
    skipped = 0
    for job in raw_jobs:
        try:
            normalized.append(normalize_remotive(job))
        except (KeyError, ValidationError, AttributeError) as e:
            skipped += 1
            print(f"Пропущена запись {job.get('id')}: {e}")

    if skipped:
        print(f"Пропущено записей: {skipped} из {len(raw_jobs)}")

    async with async_session_maker() as session:
        saved = await save_vacancy(session, "remotive", normalized)

    print(f"Сохранено новых вакансий: {saved}")


asyncio.run(collect())