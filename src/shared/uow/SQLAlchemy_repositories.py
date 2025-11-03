from src.juego.repository.sql_alchemy_jugador_repository import (
    JugadorRepositorySQLAlchemy,
)
from src.partida.repository.sql_alchemy_jugada_partida_repository import (
    PartidaJugadaRepositorySQLAlchemy,
)


class RepositoryContainer:
    def __init__(self, session):

        self._repositories = {
            "jugador": JugadorRepositorySQLAlchemy,
            "partida": PartidaJugadaRepositorySQLAlchemy,
        }
        self._session = session
        self._connected_repositories = {}
        self._connect_repositories()

    def _connect_repositories(self):
        for name, repo_class in self._repositories:
            self._connected_repositories[name] = repo_class(self._session)

    def get_repositories(self):
        return self._connected_repositories
