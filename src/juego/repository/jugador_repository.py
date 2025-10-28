from abc import ABC, abstractmethod
from typing import List, Optional
from src.shared.dbmodels.dbmodels import Jugador


class IJugadorRepository(ABC):

    @abstractmethod
    def add(self, jugador: Jugador) -> None:
        pass

    @abstractmethod
    def get_by_id(self, jugador_id: int) -> Optional[Jugador]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Jugador]:
        pass

    @abstractmethod
    def get_all(self) -> List[Jugador]:
        pass

    @abstractmethod
    def update(self, jugador: Jugador) -> None:
        pass

    @abstractmethod
    def delete(self, jugador: Jugador) -> None:
        pass
