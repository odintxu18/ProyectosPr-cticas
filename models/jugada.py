import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
class Jugada(Base):
    __tablename__ = 'jugadas'
    id = Column(Integer, primary_key=True)
    id_partida = Column(Integer, ForeignKey('partidas.id'))
    id_jugador = Column(Integer, ForeignKey('jugadores.id'))
    turno = Column(Integer, nullable=False, index=True)
    fila = Column(Integer, nullable=False)
    columna = Column(Integer, nullable=False)
    fecha_jugada = Column(DateTime, nullable=False, default=datetime.utcnow)
    partida = relationship('Partida', foreign_keys=[id_partida])
    jugador = relationship('Jugador', foreign_keys=[id_jugador])