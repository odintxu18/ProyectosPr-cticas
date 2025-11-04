from src.jugador.domain.jugador import Jugador
from src.shared.dbmodels.dbmodels import Jugador as JugadorModel
from src.partida.repository.jugador_repository import IJugadorRepository
from src.shared.sql_alchemy_interface import SqlAlchemyInterface


class SQLAlchemyJugadorRepository(IJugadorRepository, SqlAlchemyInterface):
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
