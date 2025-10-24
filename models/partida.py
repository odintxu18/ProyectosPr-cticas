from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Partida(Base):
    __tablename__ = 'partidas'
    id = Column(Integer, primary_key=True)
    id_jugador_x = Column(Integer, Foreign_key=("jugadores.id"))
    id_jugador_o = Column(Integer, Foreign_key=("jugadores.id"))
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String, nullable=False, default="en curso")
    id_ganador = Column(Integer, ForeignKey("jugadores.id"), nullable=True)
    jugador_x = relationship("Jugador", foreign_keys=[id_jugador_x])
    jugador_o = relationship("Jugador", foreign_keys=[id_jugador_o])
    ganador = relationship("Jugador", foreign_keys=[id_ganador])