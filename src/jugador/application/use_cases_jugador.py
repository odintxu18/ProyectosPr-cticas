import uuid
import re
from src.jugador.domain.jugador import Jugador
from src.jugador.repository.jugador_repository import IJugadorRepository


def new_player(nombre: str, correo: str, jugador_repo: IJugadorRepository):
    jugador = Jugador(id=str(uuid.uuid4()), nombre=nombre, correo=correo)
    jugador_repo.add(jugador)


def vaidate_email(correo: str):
    pattern = re.compile(
        "^[a-zA-Z 0-9^a-zA-Z0-9.\-_#~!$%&'*+/=?^{|}]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    )
    if not pattern.match(correo):
        raise Exception("Correo no es valido")

    return True


def actualiazar_jugador(
    jugador: Jugador, nombre: str, correo: str, jugador_repo: IJugadorRepository
):
    jugador = jugador_repo.get_by_id(jugador.id)
    jugador.correo = correo
    jugador.nombre = nombre
    jugador_repo.update(jugador)


def delete_jugador(jugador: Jugador, jugador_repo: IJugadorRepository):
    jugador_repo.delete(jugador.id)
