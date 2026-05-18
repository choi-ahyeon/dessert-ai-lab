from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Numeric, Boolean, SmallInteger, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Fruit(Base):
    __tablename__ = "fruits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_en = Column(String, nullable=False)
    name_ko = Column(String, nullable=True)
    flavordb_id = Column(Integer, nullable=False)
    sugar_per_100g = Column(Numeric, nullable=True)
    ph = Column(Numeric, nullable=True)
    ph_verified = Column(Boolean, default=False)
    citric_acid = Column(Numeric, nullable=True)
    citric_acid_verified = Column(Boolean, default=False)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)

    compounds = relationship("FruitCompound", back_populates="fruit")


class FruitCompound(Base):
    __tablename__ = "fruit_compounds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fruit_id = Column(UUID(as_uuid=True), ForeignKey("fruits.id"), nullable=False)
    pubchem_id = Column(Integer, nullable=False)
    compound_name = Column(String, nullable=True)
    flavor_profile = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)

    fruit = relationship("Fruit", back_populates="compounds")


class Combination(Base):
    __tablename__ = "combinations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fruit_a_id = Column(UUID(as_uuid=True), ForeignKey("fruits.id"), nullable=False)
    fruit_b_id = Column(UUID(as_uuid=True), ForeignKey("fruits.id"), nullable=False)
    shared_compounds = Column(Integer, nullable=True)
    compound_score = Column(Numeric, nullable=True)
    predicted_sugar = Column(Numeric, nullable=True)
    predicted_ph = Column(Numeric, nullable=True)
    predicted_flavor = Column(Text, nullable=True)
    llm_description = Column(Text, nullable=True)
    llm_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=True)

    validations = relationship("Validation", back_populates="combination")


class Validation(Base):
    __tablename__ = "validations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    combination_id = Column(UUID(as_uuid=True), ForeignKey("combinations.id"), nullable=False)
    tester_name = Column(String, nullable=False)
    sweetness = Column(SmallInteger, nullable=True)
    sourness = Column(SmallInteger, nullable=True)
    bitterness = Column(SmallInteger, nullable=True)
    saltiness = Column(SmallInteger, nullable=True)
    umami = Column(SmallInteger, nullable=True)
    balance_score = Column(SmallInteger, nullable=True)
    result = Column(String, nullable=True)
    memo = Column(Text, nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    combination = relationship("Combination", back_populates="validations")