import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

SUPERJOB_URL = "https://api.superjob.ru/2.0/vacancies/"


async def fetch_superjob_jobs() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            SUPERJOB_URL,
            headers={"X-Api-App-Id": settings.SUPERJOB_SECRET_KEY},
            params={"keyword": "python", "count": 50, "page": 0},
        )
        response.raise_for_status()
        payload = response.json()

    jobs = payload.get("objects", [])

    logger.info(
        "SuperJob отдал записей: %d, всего по запросу: %d",
        len(jobs),
        payload.get("total", 0),
    )

    return jobs