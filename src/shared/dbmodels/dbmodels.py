from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String

from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.shared.dbmodels.database import Base
from sqlalchemy.orm import relationship


class Jugada(Base):
    __tablename__ = "jugadas"
    id = Column(String, primary_key=True)
    id_partida = Column(String, ForeignKey("partidas.id"))
    id_jugador = Column(String, ForeignKey("jugadores.id"))
    turno = Column(Integer, nullable=False, index=True)
    fila = Column(Integer, nullable=False)
    columna = Column(Integer, nullable=False)
    fecha_jugada = Column(DateTime, nullable=False, default=datetime)
    partida = relationship("Partida", foreign_keys=[id_partida])
    jugador = relationship("Jugador", foreign_keys=[id_jugador])


class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    correo = Column(String, unique=True, nullable=False)


class Partida(Base):
    __tablename__ = "partidas"
    id = Column(String, primary_key=True)
    id_jugador_x = Column(String, ForeignKey("jugadores.id"))
    id_jugador_o = Column(String, ForeignKey("jugadores.id"))
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    id_ganador = Column(String, ForeignKey("jugadores.id"), nullable=True)
    jugador_x = relationship("Jugador", foreign_keys=[id_jugador_x])
    jugador_o = relationship("Jugador", foreign_keys=[id_jugador_o])
    ganador = relationship("Jugador", foreign_keys=[id_ganador])
