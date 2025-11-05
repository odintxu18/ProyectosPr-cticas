from abc import ABC, abstractmethod
from src.jugador.domain.jugador import Jugador


class IJugadorRepository(ABC):
    @abstractmethod
    def get_jugador_by_email(self, correo: str) -> Jugador | None:
        pass
