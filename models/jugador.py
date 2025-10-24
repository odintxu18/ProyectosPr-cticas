from sqlalchemy import Column, Integer, String
from database import Base

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    partidas_ganadas = Column(Integer, default=0)
    partidas_perdidas = Column(Integer, default=0)