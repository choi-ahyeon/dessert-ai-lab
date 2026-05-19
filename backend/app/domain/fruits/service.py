from sqlalchemy.orm import Session
from app.models import Fruit, FruitCompound, Combination
import uuid
from datetime import datetime, timezone

def get_all_fruits(db: Session):
    return db.query(Fruit).all()

def get_fruit_by_id(db: Session, fruit_id: str):
    return db.query(Fruit).filter(Fruit.id == fruit_id).first()

def calculate_pairing(db: Session, fruit_a_id: str, fruit_b_id: str):

    compounds_a = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_a_id
    ).all()

    compounds_b = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_b_id
    ).all()

    ids_a = set(c.pubchem_id for c in compounds_a)
    ids_b = set(c.pubchem_id for c in compounds_b)
    shared = ids_a & ids_b

    if len(ids_a) == 0 or len(ids_b) == 0:
        score = 0.0
    else:
        score = round(len(shared) / min(len(ids_a), len(ids_b)) * 100, 2)

    combination = Combination(
        id=uuid.uuid4(),
        fruit_a_id=fruit_a_id,
        fruit_b_id=fruit_b_id,
        shared_compounds=len(shared),
        compound_score=score,
        created_at=datetime.now(timezone.utc)
    )
    db.add(combination)
    db.commit()
    db.refresh(combination)

    return combination