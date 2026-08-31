

import httpx


async def fetch_remotive_jobs() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get("https://remotive.com/api/remote-jobs", params={'search': 'python', 'limit': 50})
        response.raise_for_status()
        results = response.json().get("jobs", [])
        return results