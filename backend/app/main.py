from fastapi import FastAPI
from app.database import engine, Base
from app import models

app = FastAPI(
    title="Dessert AI Lab",
    description="과일 페어링 AI 서비스",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Dessert AI Lab API 🍓"}

@app.get("/health")
async def health():
    return {"status": "ok"}