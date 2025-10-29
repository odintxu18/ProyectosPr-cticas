# src/persistance/repositories/jugador_repository_sqlalchemy.py

from sqlalchemy.orm import Session
from typing import List, Optional
from src.shared.dbmodels.dbmodels import Jugador as JugadorModel
from src.juego.repository.jugador_repository import IJugadorRepository
from test import jugador


class JugadorRepositorySQLAlchemy(IJugadorRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, datos: dict) -> dict:
        campos_validos = {c.name for c in JugadorModel.__table__.columns}
        datos_filtrados = {k: v for k, v in datos.items() if k in campos_validos}
        jugador = JugadorModel(**datos_filtrados)
        self.session.add(jugador)
        self.session.commit()
        self.session.refresh(jugador)
        return {
            column.name: getattr(jugador, column.name)
            for column in JugadorModel.__table__.columns
        }

    def get_by_id(self, filtros: str) -> Optional[dict]:
        jugador = self.session.query(JugadorModel).filter_by(**filtros).first()
        if jugador:
            return {
                column.name: getattr(jugador, column.name)
                for column in JugadorModel.__table__.columns
            }

    def get_by_nombre(self, filtros: dict) -> Optional[dict]:
        jugador = self.session.query(JugadorModel).filter_by(**filtros).first()
        if jugador:
            return {
                column.name: getattr(jugador, column.name)
                for column in JugadorModel.__table__.columns
            }

    def get_all(self, filtros: dict) -> List[dict]:
        jugador = self.session.query(JugadorModel).filter_by(**filtros).all()
        return [
            {
                column.name: getattr(p, column.name)
                for column in JugadorModel.__table__.columns
            }
            for p in jugador
        ]

    def update(self, filtros: dict, nuevos: dict) -> bool:
        try:
            resultado = (
                self.session.query(JugadorModel)
                .filter_by(**filtros)
                .update(nuevos, synchronize_session=False)
            )
            self.session.commit()
            return resultado > 0
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, filtros: dict) -> bool:
        try:
            resultado = self.session.query(JugadorModel).filter_by(**filtros).delete()
            self.session.commit()
            return resultado > 0
        except Exception as e:
            self.session.rollback()
            raise e
