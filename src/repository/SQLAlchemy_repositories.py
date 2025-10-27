from . import sql_alchemy_jugador_repository, Jugada_partida_repository
from .Jugada_partida_repository import IPartidaJugadaRepository
from .jugador_repository import IJugadorRepository
from .sql_alchemy_jugador_repository import JugadorRepositorySQLAlchemy

from .sql_alchemy_jugada_partida_repository import PartidaJugadaRepositorySQLAlchemy


class RepositoryContainer:
    def __init__(self, session):
        # Instanciamos los repositorios con la sesión
        self.jugadores: IJugadorRepository = (
            sql_alchemy_jugador_repository.JugadorRepositorySQLAlchemy(session)
        )
        self.partidas_jugadas: IPartidaJugadaRepository = (
            Jugada_partida_repository.JugadaPartidaRepositorySQLAlchemy(session)
        )
        # aquí puedes añadir más repositorios sin tocar la UoW
