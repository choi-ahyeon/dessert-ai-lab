from sqlalchemy.orm import Session
from app.models import Validation
import uuid
from datetime import datetime, timezone

def create_validation(db: Session, data):
    validation = Validation(
        id=uuid.uuid4(),
        combination_id=data.combination_id,
        tester_name=data.tester_name,
        sweetness=data.sweetness,
        sourness=data.sourness,
        bitterness=data.bitterness,
        saltiness=data.saltiness,
        umami=data.umami,
        balance_score=data.balance_score,
        result=data.result,
        memo=data.memo,
        validated_at=datetime.now(timezone.utc)
    )
    db.add(validation)
    db.commit()
    db.refresh(validation)
    return validation