from typing import List, Optional

from src.jugador.domain.jugador import Jugador
from src.shared.dbmodels.dbmodels import Jugador as JugadorModel
from src.jugador.repository.jugador_repository import IJugadorRepository
from src.shared.sql_alchemy_interface import SqlAlchemyInterface

from src.shared.dbmodels.dbmodels import *


class JugadorRepositorySQLAlchemy(IJugadorRepository, SqlAlchemyInterface):

    def get_by_nombre(self, nombre: str) -> Optional[Jugador]:
        pass

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

    def get_jugador_by_email(self, email: str) -> Jugador | None:
        jugador_model = (
            self.session.query(JugadorModel)
            .filter(JugadorModel.correo == email)
            .first()
        )
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
