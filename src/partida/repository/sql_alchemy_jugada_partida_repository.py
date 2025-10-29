from sqlalchemy import insert, Integer
from sqlalchemy.orm import Session
from typing import Optional, Any
from src.shared.dbmodels.dbmodels import (
    Partida as PartidaModel,
    Jugada as JugadaModel,
    Partida,
)
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository


class PartidaJugadaRepositorySQLAlchemy(IPartidaJugadaRepository):

    def __init__(self, session: Session):
        self.session = session

    def agregar_partida(self, datos: dict) -> str:

        partida = PartidaModel(**datos)
        self.session.add(partida)
        self.session.commit()

        return datos["id"]

    def obtener_partida(self, filtros: str) -> Optional[dict]:
        partida = self.session.query(PartidaModel).filter_by(**filtros).first()
        if partida:
            return {
                column.name: getattr(partida, column.name)
                for column in PartidaModel.__table__.columns
            }

    def obtener_partida_por_id(self, partida_id: int) -> Optional[Partida]:
        pass

    def listar_partidas(self, filtros: str) -> list[str]:
        partidas = self.session.query(PartidaModel).filter_by(**filtros).all()
        return [
            {
                column.name: getattr(p, column.name)
                for column in PartidaModel.__table__.columns
            }
            for p in partidas
        ]

    def actualizar_partida(self, filtros: dict, nuevos: dict) -> bool:
        try:
            resultado = (
                self.session.query(PartidaModel)
                .filter_by(**filtros)
                .update(nuevos, synchronize_session=False)
            )
            self.session.commit()
            return resultado > 0
        except Exception as e:
            self.session.rollback()
            raise e

    def agregar_jugada(self, datos: dict) -> str:

        jugada = JugadaModel(**datos)
        self.session.add(jugada)
        self.session.commit()
        return {
            column.name: getattr(jugada, column.name)
            for column in JugadaModel.__table__.columns
        }

    def obtener_jugada_por_id(self, filtros: dict) -> Optional[dict]:
        jugada = self.session.query(JugadaModel).filter_by(**filtros).first()
        if jugada:
            return {
                column.name: getattr(jugada, column.name)
                for column in PartidaModel.__table__.columns
            }

    def obtener_jugadas_por_partida(self, filtros: dict) -> list[dict]:

        jugadas = self.session.query(JugadaModel).filter_by(**filtros).all()
        return [
            {
                column.name: getattr(jugada, column.name)
                for column in JugadaModel.__table__.columns
            }
            for jugada in jugadas
        ]

    def eliminar_jugada(self, filtros: dict) -> bool:
        try:
            resultado = self.session.query(JugadaModel).filter_by(**filtros).delete()
            self.session.commit()
            return resultado > 0
        except Exception as e:
            self.session.rollback()
            raise e
