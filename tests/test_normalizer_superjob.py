import pytest

from app.normalizers.superjob import normalize_superjob


def make_raw(**overrides) -> dict:
    """Сырая запись в формате SuperJob. Любой ключ можно переопределить."""
    raw = {
        "id": 52258175,
        "profession": "Python-разработчик",
        "firm_name": "VK: Старт карьеры",
        "town": {"id": 4, "title": "Москва", "declension": "в Москве"},
        "link": "https://www.superjob.ru/vakansii/python-razrabotchik-52258175.html",
        "payment_from": 200000,
        "payment_to": 300000,
        "currency": "rub",
    }
    raw.update(overrides)
    return raw


def test_normalize_maps_fields():
    vacancy = normalize_superjob(make_raw())

    assert vacancy.external_id == "52258175"
    assert vacancy.title == "Python-разработчик"
    assert vacancy.company == "VK: Старт карьеры"
    assert vacancy.city == "Москва"
    assert vacancy.url == "https://www.superjob.ru/vakansii/python-razrabotchik-52258175.html"
    assert vacancy.salary_min == 200000


def test_numeric_id_becomes_string():
    assert normalize_superjob(make_raw()).external_id == "52258175"


def test_zero_payment_becomes_none():
    """SuperJob присылает 0, когда зарплата не указана. Ноль не должен попасть в базу."""
    assert normalize_superjob(make_raw(payment_from=0)).salary_min is None


def test_missing_town_gives_none_city():
    raw = make_raw()
    del raw["town"]

    assert normalize_superjob(raw).city is None


def test_empty_town_title_gives_none_city():
    assert normalize_superjob(make_raw(town={"id": 4, "title": ""})).city is None


def test_client_title_used_when_firm_name_empty():
    raw = make_raw(firm_name="", client={"id": 4904563, "title": "VK: Старт карьеры"})

    assert normalize_superjob(raw).company == "VK: Старт карьеры"


def test_missing_profession_raises_key_error():
    raw = make_raw()
    del raw["profession"]

    with pytest.raises(KeyError):
        normalize_superjob(raw)