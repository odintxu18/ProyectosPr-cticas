from src.partida.repository.sql_alchemy_jugada_partida_repository import (
    PartidaJugadaRepositorySQLAlchemy,
)
from src.partida.repository.sql_alchemy_jugador_repository import (
    SQLAlchemyJugadorRepository,
)

partida_dependencies = {
    "jugador": SQLAlchemyJugadorRepository,
    "partida": PartidaJugadaRepositorySQLAlchemy,
}
