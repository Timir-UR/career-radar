from fastapi import FastAPI

from app.api.vacancies import router as vacancies_router
from app.web.pages import router as pages_router

app = FastAPI(title="Career Radar")

app.include_router(vacancies_router)
app.include_router(pages_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}