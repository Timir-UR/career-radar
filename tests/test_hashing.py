from app.dedup.hashing import make_content_hash
from app.schemas.vacancy import NormalizeVacancy


def make_vacancy(
    company: str = "Lemon.io",
    title: str = "Backend Developer",
    city: str | None = "Europe",
) -> NormalizeVacancy:
    """Собрать вакансию для теста. Незаданные поля получают заглушки."""
    return NormalizeVacancy(
        external_id="1",
        title=title,
        company=company,
        city=city,
        url="https://example.com/1",
        salary_min=20000,
    )


def test_same_data_gives_same_hash():
    first = make_vacancy()
    second = make_vacancy()

    assert make_content_hash(first) == make_content_hash(second)


def test_same_different_same_hash():
    first = make_vacancy(company="Lemon.io")
    second = make_vacancy(company="LEMON.IO")

    assert make_content_hash(first) == make_content_hash(second)


def test_same_space_same_hash():
    first = make_vacancy(company="  Lemon.io")
    second = make_vacancy(company="Lemon.io")

    assert make_content_hash(first) == make_content_hash(second)


def test_same_different_company_same_different_hash():
    first = make_vacancy(company="Lemon.io")
    second = make_vacancy(company="AMC")

    assert make_content_hash(first) != make_content_hash(second)


def test_same_different_name_same_different_hash():
    first = make_vacancy(title="back")
    second = make_vacancy(title="front")

    assert make_content_hash(first) != make_content_hash(second)


def test_same_city_same_hash():
    first = make_vacancy(city="")
    second = make_vacancy(city=None)

    assert make_content_hash(first) == make_content_hash(second)


def test_hash_length_is_64():
    assert len(make_content_hash(make_vacancy())) == 64
