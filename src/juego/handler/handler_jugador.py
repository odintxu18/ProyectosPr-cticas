from src.juego.domain.jugador import Jugador
from src.juego.repository.jugador_repository import IJugadorRepository
from src.shared.uow.unit_of_work import IUnitOfWork
from src.juego.applicacion.use_cases.use_cases_jugador import (
    new_player,
    vaidate_email,
    actualiazar_jugador,
    delete_jugador,
)


class JugadorHandler:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def crear_jugador(self, nombre: str, correo: str):
        vaidate_email(correo)
        jugador_repo: IJugadorRepository = self.uow.get_repository("jugador")
        new_player(nombre, correo, jugador_repo)

        self.uow.commit()

    def actualizar_jugador(self, id_jugador: str, nombre: str, correo: str):
        vaidate_email(correo)
        jugador_repo: IJugadorRepository = self.uow.get_repository("jugador")
        jugador = jugador_repo.get_by_id(id_jugador)
        if not jugador:
            raise Exception("Jugador no encontrado")

        actualiazar_jugador(jugador, nombre, correo, jugador_repo)
        self.uow.commit()

    def eliminar_jugador(self, id_jugador: str):
        jugador_repo: IJugadorRepository = self.uow.get_repository("jugador")
        jugador = jugador_repo.get_by_id(id_jugador)
        if not jugador:
            raise Exception("Jugador no encontrado")

        delete_jugador(jugador, jugador_repo)
        self.uow.commit()
