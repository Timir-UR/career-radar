

from fastapi import FastAPI


app = FastAPI(title="Career Radar")

@app.get("/health")
async def health_check():
    return {"status": "ok"}