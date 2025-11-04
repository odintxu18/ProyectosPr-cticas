from src.partida.repository.sql_alchemy_jugador_repository import (
    SQLAlchemyJugadorRepository,
)

jugador_dependencies = {
    "jugador": SQLAlchemyJugadorRepository,
}
