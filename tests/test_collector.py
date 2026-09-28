from app.collectors.filter_python_jobs import filter_python_jobs


def make_job(**overrides) -> dict:
    """Сырая запись в формате Remotive. Любой ключ можно переопределить."""
    raw = {
        "title": "Senior Developer",
        "description": "work and work"
    }
    raw.update(overrides)
    return raw


def test_python_in_title_matches():
    jobs = [make_job(title="python developer")]

    assert filter_python_jobs(jobs) == jobs

def test_python_in_description_matches():
    jobs = [make_job(description="pythoner")]

    assert filter_python_jobs(jobs) == jobs

def test_python_in_out_matches():
    jobs = [make_job()]

    assert filter_python_jobs(jobs) ==[]

def test_python_in_description_caps_matches():
    jobs = [make_job(description="Pythoner")]

    assert filter_python_jobs(jobs) == jobs

def test_python_in_out_all_matches():
    jobs = [{}]

    assert filter_python_jobs(jobs) == []

def test_python_in_same_jobs_matches():
    jobs = [make_job(title="Pythoner"), make_job(title="Senior"),
            make_job(title="Senior Python Developer")]
    result = filter_python_jobs(jobs)


    assert [job["title"] for job in result] == ["Pythoner", "Senior Python Developer"]
