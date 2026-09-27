import pytest

from app.normalizers.remotive import normalize_remotive


def make_raw(**overrides) -> dict:
    """Сырая запись в формате Remotive. Любой ключ можно переопределить."""
    raw = {
        "id": 2091141,
        "title": "Senior Python Developer",
        "company_name": "Lemon.io",
        "candidate_required_location": "Europe",
        "url": "https://example.com/remote-jobs/2091141",
    }
    raw.update(overrides)
    return raw


def test_normalize_maps_fields():
    vacancy = normalize_remotive(make_raw())
    assert vacancy.title == "Senior Python Developer"
    assert vacancy.company == "Lemon.io"
    assert vacancy.url == "https://example.com/remote-jobs/2091141"


def test_numeric_id_becomes_string():
    vacancy = normalize_remotive(make_raw())

    assert vacancy.external_id == "2091141"
    assert isinstance(vacancy.external_id, str)


def test_missing_city_gives_none():
    raw = make_raw()
    del raw["candidate_required_location"]

    vacancy = normalize_remotive(raw)

    assert vacancy.city is None


def test_missing_title_raises_key_error():
    raw = make_raw()
    del raw["title"]

    with pytest.raises(KeyError):
        normalize_remotive(raw)


def test_salary_is_always_none():
    """Парсер зарплат не написан: поле всегда пустое, даже если источник дал значение."""
    raw = make_raw(salary="$90k - $105k")

    vacancy = normalize_remotive(raw)

    assert vacancy.salary_min is None
