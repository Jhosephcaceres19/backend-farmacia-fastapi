from sqlalchemy import Column, Integer,String, Float

from src.database import Base

class Farmacia(Base):
    __tablename__ = "farmacia"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    price = Column(Float)
    score = Column(Integer)
    description = Column(String, nullable=True)
