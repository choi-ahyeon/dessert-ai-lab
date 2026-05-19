from pydantic import BaseModel
from typing import Optional
import uuid

class ValidationCreate(BaseModel):
    combination_id: str
    tester_name: str
    sweetness: int
    sourness: int
    bitterness: int
    saltiness: int
    umami: int
    balance_score: int
    result: str
    memo: Optional[str] = None

class ValidationResponse(BaseModel):
    id: uuid.UUID
    combination_id: uuid.UUID
    tester_name: str
    sweetness: Optional[int]
    sourness: Optional[int]
    bitterness: Optional[int]
    saltiness: Optional[int]
    umami: Optional[int]
    balance_score: Optional[int]
    result: Optional[str]
    memo: Optional[str]

    class Config:
        from_attributes = True