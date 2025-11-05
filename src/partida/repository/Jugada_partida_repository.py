from abc import ABC, abstractmethod
from typing import List, Optional

from src.partida.domain.jugada import Jugada
from src.partida.domain.partida import Partida


class IPartidaJugadaRepository(ABC):
    @abstractmethod
    def agregar_partida(self, partida: Partida) -> Partida:
        pass

    @abstractmethod
    def obtener_partida_por_id(self, partida_id: str) -> Optional[Partida]:
        pass

    @abstractmethod
    def listar_partidas(self) -> List[Partida]:
        pass

    @abstractmethod
    def actualizar_partida(self, partida: Partida) -> Partida:
        pass

    @abstractmethod
    def agregar_jugada(self, jugada: Jugada) -> Jugada:
        pass

    @abstractmethod
    def obtener_jugadas_por_partida(self, partida_id: str) -> List[Jugada]:
        pass

    @abstractmethod
    def obtener_jugada_por_id(self, jugada_id: str) -> Optional[Jugada]:
        pass

    @abstractmethod
    def eliminar_jugada(self, jugada: Jugada) -> None:
        pass
