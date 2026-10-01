import asyncio
import logging

import httpx
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.collectors.remotive import fetch_remotive_jobs
from app.collectors.superjob import fetch_superjob_jobs
from app.core.config import settings
from app.db.storage import get_source, save_vacancy
from app.normalizers.remotive import normalize_remotive
from app.normalizers.superjob import normalize_superjob
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


async def collect_data(source_name: str) -> int:
    if source_name == "remotive":
        collector = fetch_remotive_jobs
        normalizer = normalize_remotive
    elif source_name == "superjob":
        collector = fetch_superjob_jobs
        normalizer = normalize_superjob
    else:
        raise ValueError(f"Неизвестный источник: {source_name}")

    engine = create_async_engine(settings.database_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_maker() as session:
            source = await get_source(session, source_name)
            if source is None:
                logger.error("[%s] Источник не найден в базе", source_name)
                return 0
            if not source.enabled:
                logger.info("[%s] Источник отключён, пропуск сбора", source_name)
                return 0

            raw_jobs = await collector()
            logger.info("[%s] Получено подходящих вакансий: %d", source_name, len(raw_jobs))

            normalized = []
            skipped = 0
            for job in raw_jobs:
                try:
                    normalized.append(normalizer(job))
                except (KeyError, ValidationError, AttributeError) as e:
                    skipped += 1
                    logger.warning("[%s] Пропущена запись %s: %s", source_name, job.get("id"), e)

            if skipped:
                logger.info(
                    "[%s] Пропущено записей: %d из %d", source_name, skipped, len(raw_jobs)
                )

            saved = await save_vacancy(session, source, normalized)
            source.last_run_at = func.now()
            await session.commit()
    finally:
        await engine.dispose()

    logger.info("[%s] Сохранено новых вакансий: %d", source_name, saved)
    return saved


@celery_app.task(
    autoretry_for=(httpx.HTTPError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=1,
)
def collect_remotive() -> int:
    return asyncio.run(collect_data("remotive"))


@celery_app.task(
    autoretry_for=(httpx.HTTPError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=3,
)
def collect_superjob() -> int:
    return asyncio.run(collect_data("superjob"))