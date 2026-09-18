import asyncio
from sqlalchemy import func
from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import httpx
import logging
from app.db.storage import get_source, save_vacancy
from app.normalizers.remotive import normalize_remotive
from pydantic import ValidationError
from app.tasks.celery_app import celery_app
from app.collectors.remotive import fetch_remotive_jobs

logger = logging.getLogger(__name__)


async def collect_data():
    engine = create_async_engine(settings.database_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_maker() as session:
            source = await get_source(session, "remotive")
            if source is None:
                logger.error("Источник 'remotive' не найден в базе")
                return 0
            if not source.enabled:
                logger.info("Источник 'remotive' отключен, пропуск сбора данных")
                return 0
            raw_jobs = await fetch_remotive_jobs()
            logger.info("Получено записей: %d", len(raw_jobs))

            normalized = []
            skipped = 0
            for job in raw_jobs:
                try:
                    normalized.append(normalize_remotive(job))
                except (KeyError, ValidationError, AttributeError) as e:
                    skipped += 1
                    logger.warning("Пропущена запись %s: %s", job.get("id"), e)
            if skipped:
                logger.info("Пропущено записей: %d из %d", skipped, len(raw_jobs))
            saved = await save_vacancy(session, source, normalized)
            source.last_run_at = func.now()
            await session.commit()
    finally:
        await engine.dispose()

    logger.info("Сохранено новых вакансий: %d", saved)
    return saved


@celery_app.task(
    autoretry_for=(httpx.HTTPError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=3,
)
def collect_vacancies():

    return asyncio.run(collect_data())
