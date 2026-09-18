from app.api.vacancies import router
from fastapi import FastAPI


app = FastAPI(title="Career Radar")
app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
