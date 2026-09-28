def filter_python_jobs(jobs: list[dict]) -> list[dict]:
    python_jobs = []
    for job in jobs:
        title = job.get("title", "")
        description = job.get("description", "")

        text = f"{title} {description}".lower()

        if "python" in text:
            python_jobs.append(job)

    return python_jobs