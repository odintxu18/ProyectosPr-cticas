# src/persistance/repositories/jugador_repository_sqlalchemy.py
from pygments.lexers import j
from sqlalchemy.orm import Session
from typing import List, Optional

from src.juego.domain.jugador import Jugador
from src.shared.dbmodels.dbmodels import Jugador as JugadorModel
from src.juego.repository.jugador_repository import IJugadorRepository
from test import jugador
from src.shared.dbmodels.dbmodels import *


class FakeJugadorRepositorySQLAlchemy(IJugadorRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, player: Jugador) -> Jugador:

        jugador_model = JugadorModel(
            id=player.id,
            nombre=player.nombre,
            correo=player.correo,
        )
        self.session.add(jugador_model)
        self.session.commit()

        return Jugador(
            id=jugador_model.id,
            nombre=jugador_model.nombre,
            correo=jugador_model.correo,
        )

    def get_by_id(self, id_jugador: str) -> Jugador | None:
        jugador_model = self.session.get(JugadorModel, id_jugador)
        if jugador_model:
            return Jugador(
                id=jugador_model.id,
                nombre=jugador_model.nombre,
                correo=jugador_model.correo,
            )
        return None

    def get_by_nombre(self, nombre_jugador: str) -> Jugador:
        jugador_model = self.session.get(JugadorModel, nombre_jugador)
        if jugador_model:
            return Jugador(
                id=jugador_model.id,
                nombre=jugador_model.nombre,
                correo=jugador_model.correo,
            )
        return None

    def get_all(self) -> List[Jugador]:
        jugadores = self.session.query(Jugador).all()

        return [
            Jugador(
                id=j.id,
                nombre=j.nombre,
                correo=j.correo,
            )
            for j in jugadores
        ]

    def update(self, jugador: Jugador) -> bool:
        try:
            actualizado = (
                self.session.query(JugadorModel)
                .filter_by(id=jugador.id)
                .update(
                    {"nombre": jugador.nombre, "correo": jugador.correo},
                    synchronize_session=False,
                )
            )
            self.session.commit()
            return actualizado > 0
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_jugador: str) -> bool:
        try:
            eliminado = (
                self.session.query(JugadorModel).filter_by(id=id_jugador).delete()
            )
            self.session.commit()
            return eliminado > 0
        except Exception as e:
            self.session.rollback()
            raise e
