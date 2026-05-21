from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.domain.fruits.router import router as fruits_router
from app.domain.validations.fruitmatch.router import router as validations_fruitmatch_router

app = FastAPI(
    title="Dessert AI Lab",
    description="과일 페어링 AI 서비스",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://renovator-rubber-pony.ngrok-free.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(fruits_router)
app.include_router(validations_fruitmatch_router)

@app.get("/")
async def root():
    return {"message": "Dessert AI Lab API 🍓"}

@app.get("/health")
async def health():
    return {"status": "ok"}