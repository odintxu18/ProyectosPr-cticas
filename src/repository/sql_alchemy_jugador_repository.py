# src/persistance/repositories/jugador_repository_sqlalchemy.py

from sqlalchemy.orm import Session
from typing import List, Optional
from src.persistance.models.dbmodels import Jugador
from src.repository.jugador_repository import IJugadorRepository


class JugadorRepositorySQLAlchemy(IJugadorRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, jugador: Jugador) -> None:
        self.session.add(jugador)

    def get_by_id(self, jugador_id: int) -> Optional[Jugador]:
        return self.session.query(Jugador).filter_by(id=jugador_id).first()

    def get_by_nombre(self, nombre: str) -> Optional[Jugador]:
        return self.session.query(Jugador).filter_by(nombre=nombre).first()

    def get_all(self) -> List[Jugador]:
        return self.session.query(Jugador).all()

    def update(self, jugador: Jugador) -> None:
        self.session.merge(jugador)

    def delete(self, jugador: Jugador) -> None:
        self.session.delete(jugador)
