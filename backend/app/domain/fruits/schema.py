from pydantic import BaseModel
from typing import Optional
import uuid

class FruitResponse(BaseModel):
    id: uuid.UUID
    name_en: str
    name_ko: Optional[str]
    flavordb_id: int
    category: Optional[str]
    ph: Optional[float]
    ph_verified: Optional[bool] = None
    sugar_per_100g: Optional[float]

    class Config:
        from_attributes = True

class PairingRequest(BaseModel):
    fruit_a_id: str
    fruit_b_id: str

class PairingResponse(BaseModel):
    id: uuid.UUID
    fruit_a_id: uuid.UUID
    fruit_b_id: uuid.UUID
    shared_compounds: Optional[int]
    compound_score: Optional[float]
    predicted_sugar: Optional[float]
    predicted_ph: Optional[float]
    llm_description: Optional[str]
    llm_verified: Optional[bool]

    class Config:
        from_attributes = True