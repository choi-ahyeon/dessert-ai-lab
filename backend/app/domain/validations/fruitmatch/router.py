from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.domain.validations.fruitmatch import service
from app.domain.validations.fruitmatch.schema import ValidationCreate, ValidationResponse

router = APIRouter(
    prefix="/validations/fruitmatch",
    tags=["validations"]
)

@router.post("/", response_model=ValidationResponse)
def create_validation(request: ValidationCreate, db: Session = Depends(get_db)):
    return service.create_validation(db, request)