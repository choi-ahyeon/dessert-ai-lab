from sqlalchemy.orm import Session
from app.models import Fruit, FruitCompound, Combination
import uuid
from datetime import datetime, timezone

def get_all_fruits(db: Session):
    return db.query(Fruit).all()

def get_fruit_by_id(db: Session, fruit_id: str):
    return db.query(Fruit).filter(Fruit.id == fruit_id).first()

def predict_mix(fruit_a: Fruit, fruit_b: Fruit):
    predicted_sugar = None
    predicted_ph = None

    if fruit_a.sugar_per_100g and fruit_b.sugar_per_100g:
        predicted_sugar = round((float(fruit_a.sugar_per_100g) + float(fruit_b.sugar_per_100g)) / 2, 2)

    if fruit_a.ph and fruit_b.ph:
        predicted_ph = round((float(fruit_a.ph) + float(fruit_b.ph)) / 2, 2)

    return predicted_sugar, predicted_ph

def calculate_pairing(db: Session, fruit_a_id: str, fruit_b_id: str):

    compounds_a = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_a_id
    ).all()

    compounds_b = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_b_id
    ).all()
    fruit_a = db.query(Fruit).filter(Fruit.id == fruit_a_id).first()
    fruit_b = db.query(Fruit).filter(Fruit.id == fruit_b_id).first()

    predicted_sugar, predicted_ph = predict_mix(fruit_a, fruit_b)
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
        predicted_sugar=predicted_sugar,
        predicted_ph=predicted_ph,
        created_at=datetime.now(timezone.utc)
    )
    db.add(combination)
    db.commit()
    db.refresh(combination)

    return combination