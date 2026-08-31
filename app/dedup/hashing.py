import hashlib

from app.schemas.vacancy import NormalizeVacancy

def make_content_hash(vacancy: NormalizeVacancy) -> str:
    """Создает хэш для вакансии на основе ее содержимого."""
    company = vacancy.company.lower().strip()
    title = vacancy.title.lower().strip()
    city = vacancy.city.lower().strip() if vacancy.city else ""

    key = f"{company}|{title}|{city}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()