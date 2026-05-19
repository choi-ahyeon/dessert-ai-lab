from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.domain.fruits import service
from app.domain.fruits.schema import FruitResponse, PairingRequest, PairingResponse
from typing import List

router = APIRouter(
    prefix="/fruits",
    tags=["fruits"]
)

@router.get("/", response_model=List[FruitResponse])
def get_fruits(db: Session = Depends(get_db)):
    return service.get_all_fruits(db)

@router.get("/{fruit_id}", response_model=FruitResponse)
def get_fruit(fruit_id: str, db: Session = Depends(get_db)):
    return service.get_fruit_by_id(db, fruit_id)

@router.post("/pairing", response_model=PairingResponse)
def calculate_pairing(request: PairingRequest, db: Session = Depends(get_db)):
    return service.calculate_pairing(db, request.fruit_a_id, request.fruit_b_id)