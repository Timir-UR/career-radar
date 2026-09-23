from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import list_vacancies
from app.db.session import get_async_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

PAGE_SIZE = 20


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Главная страница: форма и первая порция вакансий."""
    vacancies = await list_vacancies(session, limit=PAGE_SIZE)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"vacancies": vacancies, "offset": 0, "limit": PAGE_SIZE},
    )


@router.get("/partials/vacancies", response_class=HTMLResponse)
async def vacancies_partial(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    q: str | None = None,
    city: str | None = None,
    company: str | None = None,
    salary_min: str | None = None,
    offset: int = 0,
):
    """Фрагмент со списком для HTMX.

    Форма браузера присылает пустые поля пустыми строками, а не отсутствием
    параметра. Поэтому всё принимается строками и приводится вручную:
    пустая строка → None, зарплата → int, если это число.
    """
    salary = int(salary_min) if salary_min and salary_min.isdigit() else None

    vacancies = await list_vacancies(
        session,
        q=q or None,
        city=city or None,
        company=company or None,
        salary_min=salary,
        limit=PAGE_SIZE,
        offset=offset,
    )
    return templates.TemplateResponse(
        request,
        "_vacancies.html",
        {"vacancies": vacancies, "offset": offset, "limit": PAGE_SIZE},
    )