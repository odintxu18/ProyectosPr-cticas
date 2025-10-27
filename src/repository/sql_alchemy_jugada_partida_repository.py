from sqlalchemy.orm import Session, Query
from typing import List, Optional, Any
from src.persistance.models.dbmodels import Partida, Jugada
from src.repository.Jugada_partida_repository import IPartidaJugadaRepository


class PartidaJugadaRepositorySQLAlchemy(IPartidaJugadaRepository):

    def __init__(self, session: Session):
        self.session = session

    def agregar_partida(self, partida: Partida) -> Partida:
        self.session.add(partida)
        return partida

    def obtener_partida_por_id(self, partida_id: int) -> Optional[Partida]:
        return self.session.query(Partida).filter_by(id=partida_id).first()

    def listar_partidas(self) -> list[type[Partida]]:
        return self.session.query(Partida).all()

    def actualizar_partida(self, partida: Partida) -> Partida:
        self.session.merge(partida)
        return partida

    def agregar_jugada(self, jugada: Jugada) -> Jugada:
        self.session.add(jugada)
        return jugada

    def obtener_jugada_por_id(self, jugada_id: int) -> Optional[Jugada]:
        return self.session.query(Jugada).filter_by(id=jugada_id).first()

    def obtener_jugadas_por_partida(self, partida_id: int) -> list[type[Jugada]]:
        return (
            self.session.query(Jugada)
            .filter_by(id_partida=partida_id)
            .order_by(Jugada.turno.asc())
            .all()
        )

    def eliminar_jugada(self, jugada: Jugada) -> None:
        self.session.delete(jugada)
