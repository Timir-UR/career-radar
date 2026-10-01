from app.schemas.vacancy import NormalizeVacancy


def normalize_remotive(raw: dict) -> NormalizeVacancy:
    return NormalizeVacancy(
        external_id=str(raw["id"]),
        title=raw["title"],
        company=raw["company_name"],
        city=raw.get("candidate_required_location"),
        url=raw["url"],
        # Remotive присылает зарплату строкой («$50,000 - $70,000»), числа нет.
        # Разбор — отдельная задача, см. бэклог.
        salary_min=None,
    )
