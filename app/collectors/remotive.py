import httpx

from app.collectors.filter_python_jobs import filter_python_jobs


async def fetch_remotive_jobs() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://remotive.com/api/remote-jobs"
        )
        response.raise_for_status()

        jobs = response.json().get("jobs", [])

        return filter_python_jobs(jobs)[:50]