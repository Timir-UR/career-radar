from pydantic import BaseModel, Field

class NormalizeVacancy(BaseModel):
    external_id: str
    title: str
    company: str
    city: str | None
    url: str
    salary_min: int | None