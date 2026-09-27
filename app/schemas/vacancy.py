from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NormalizeVacancy(BaseModel):
    external_id: str
    title: str
    company: str
    city: str | None
    url: str
    salary_min: int | None


class VacancyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    company: str
    city: str | None
    url: str
    salary_min: int | None
    first_seen_at: datetime
