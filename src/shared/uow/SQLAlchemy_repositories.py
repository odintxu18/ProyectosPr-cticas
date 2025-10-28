from src.juego.repository import sql_alchemy_jugador_repository
from src.partida.repository import Jugada_partida_repository
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.juego.repository.jugador_repository import IJugadorRepository


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
