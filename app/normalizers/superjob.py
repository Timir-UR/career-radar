from app.schemas.vacancy import NormalizeVacancy


def normalize_superjob(raw: dict) -> NormalizeVacancy:
    town = raw.get("town") or {}
    client = raw.get("client") or {}

    return NormalizeVacancy(
        external_id=str(raw["id"]),
        title=raw["profession"],
        company=raw.get("firm_name") or client.get("title") or None,
        city=town.get("title") or None,
        url=raw["link"],
        salary_min=raw.get("payment_from") or None,
    )