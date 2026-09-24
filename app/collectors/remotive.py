import httpx

async def fetch_remotive_jobs() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://remotive.com/api/remote-jobs"
        )
        response.raise_for_status()

        jobs = response.json().get("jobs", [])

        python_jobs = []

        for job in jobs:
            title = job.get("title", "")
            description = job.get("description", "")

            text = f"{title} {description}".lower()

            if "python" in text:
                python_jobs.append(job)

        return python_jobs[:50]