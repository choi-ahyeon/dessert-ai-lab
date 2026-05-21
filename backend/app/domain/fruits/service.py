from sqlalchemy.orm import Session
from app.models import Fruit, FruitCompound, Combination
import uuid
from datetime import datetime, timezone

def get_all_fruits(db: Session):
    return db.query(Fruit).all()

def get_fruit_by_id(db: Session, fruit_id: str):
    return db.query(Fruit).filter(Fruit.id == fruit_id).first()

def predict_mix(fruit_a: Fruit, fruit_b: Fruit, ratio_a: float = 0.5, ratio_b: float = 0.5):
    predicted_sugar = None
    predicted_ph = None
    predicted_sweetness = None
    predicted_acidity = None
    predicted_bitterness = None
    predicted_creaminess = None
    predicted_juiciness = None
    predicted_richness = None
    predicted_freshness = None

    if fruit_a.sugar_per_100g and fruit_b.sugar_per_100g:
        predicted_sugar = round(float(fruit_a.sugar_per_100g) * ratio_a + float(fruit_b.sugar_per_100g) * ratio_b, 2)

    if fruit_a.ph and fruit_b.ph:
        predicted_ph = round(float(fruit_a.ph) * ratio_a + float(fruit_b.ph) * ratio_b, 2)

    if fruit_a.sweetness_score and fruit_b.sweetness_score:
        predicted_sweetness = round(fruit_a.sweetness_score * ratio_a + fruit_b.sweetness_score * ratio_b, 2)

    if fruit_a.acidity_score and fruit_b.acidity_score:
        predicted_acidity = round(fruit_a.acidity_score * ratio_a + fruit_b.acidity_score * ratio_b, 2)

    if fruit_a.bitterness_score and fruit_b.bitterness_score:
        predicted_bitterness = round(fruit_a.bitterness_score * ratio_a + fruit_b.bitterness_score * ratio_b, 2)

    if fruit_a.creaminess_score and fruit_b.creaminess_score:
        predicted_creaminess = round(fruit_a.creaminess_score * ratio_a + fruit_b.creaminess_score * ratio_b, 2)

    if fruit_a.juiciness_score and fruit_b.juiciness_score:
        predicted_juiciness = round(fruit_a.juiciness_score * ratio_a + fruit_b.juiciness_score * ratio_b, 2)

    if fruit_a.richness_score and fruit_b.richness_score:
        predicted_richness = round(fruit_a.richness_score * ratio_a + fruit_b.richness_score * ratio_b, 2)

    if fruit_a.freshness_score and fruit_b.freshness_score:
        predicted_freshness = round(fruit_a.freshness_score * ratio_a + fruit_b.freshness_score * ratio_b, 2)

    return {
        "predicted_sugar": predicted_sugar,
        "predicted_ph": predicted_ph,
        "predicted_sweetness": predicted_sweetness,
        "predicted_acidity": predicted_acidity,
        "predicted_bitterness": predicted_bitterness,
        "predicted_creaminess": predicted_creaminess,
        "predicted_juiciness": predicted_juiciness,
        "predicted_richness": predicted_richness,
        "predicted_freshness": predicted_freshness,
    }

def calculate_pairing(db: Session, fruit_a_id: str, fruit_b_id: str, ratio_a: float = 0.5, ratio_b: float = 0.5):

    compounds_a = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_a_id
    ).all()

    compounds_b = db.query(FruitCompound).filter(
        FruitCompound.fruit_id == fruit_b_id
    ).all()

    fruit_a = db.query(Fruit).filter(Fruit.id == fruit_a_id).first()
    fruit_b = db.query(Fruit).filter(Fruit.id == fruit_b_id).first()

    ids_a = set(c.pubchem_id for c in compounds_a)
    ids_b = set(c.pubchem_id for c in compounds_b)
    shared = ids_a & ids_b

    if len(ids_a) == 0 or len(ids_b) == 0:
        score = 0.0
    else:
        score = round(len(shared) / min(len(ids_a), len(ids_b)) * 100, 2)

    mix = predict_mix(fruit_a, fruit_b, ratio_a, ratio_b)

    combination = Combination(
        id=uuid.uuid4(),
        fruit_a_id=fruit_a_id,
        fruit_b_id=fruit_b_id,
        shared_compounds=len(shared),
        compound_score=score,
        predicted_sugar=mix["predicted_sugar"],
        predicted_ph=mix["predicted_ph"],
        predicted_sweetness=mix["predicted_sweetness"],
        predicted_acidity=mix["predicted_acidity"],
        predicted_bitterness=mix["predicted_bitterness"],
        predicted_creaminess=mix["predicted_creaminess"],
        predicted_juiciness=mix["predicted_juiciness"],
        predicted_richness=mix["predicted_richness"],
        predicted_freshness=mix["predicted_freshness"],
        ratio_a=ratio_a,
        ratio_b=ratio_b,
        created_at=datetime.now(timezone.utc)
    )
    db.add(combination)
    db.commit()
    db.refresh(combination)

    return combination