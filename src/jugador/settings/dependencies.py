from src.jugador.repository.sql_alchemy_jugador_repository import (
    JugadorRepositorySQLAlchemy,
)

jugador_dependencies = {
    "jugador": JugadorRepositorySQLAlchemy,
}
