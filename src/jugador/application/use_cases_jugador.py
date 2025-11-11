import uuid
import re
from src.jugador.domain.jugador import Jugador
from src.jugador.repository.jugador_repository import IJugadorRepository


def new_player(nombre: str, correo: str, jugador_repo: IJugadorRepository) -> str:
    if not _validate_email(correo):
        raise InvalidEmailException()
    id = str(uuid.uuid4())
    jugador = Jugador(id=id, nombre=nombre, correo=correo)
    jugador_repo.add(jugador)
    return id


def _validate_email(correo: str) -> bool:
    pattern = re.compile(
        r"^[a-zA-Z 0-9^a-zA-Z0-9.\-_#~!$%&'*+/=?^{|}]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    )
    return bool(pattern.match(correo))


def actualiazar_jugador(datos_jugador: dict, jugador_repo: IJugadorRepository):
    jugador = jugador_repo.get_by_id(datos_jugador["id"])
    if not jugador:
        raise JugadorNotFound()
    if not _validate_email(datos_jugador["correo"]):
        raise InvalidEmailException()
    jugador.correo = datos_jugador["correo"]
    jugador.nombre = datos_jugador["nombre"]
    jugador_repo.update(jugador)


def delete_jugador(datos_jugador: dict, jugador_repo: IJugadorRepository):
    jugador_repo.delete(datos_jugador["id"])


def get_jugador_by_id(id_jugador: str, jugador_repo) -> dict:

    jugador = jugador_repo.get_by_id(id_jugador)
    return {
        "id": id_jugador,
        "nombre": jugador.nombre,
        "correo": jugador.correo,
    }


class InvalidEmailException(Exception):
    pass


class JugadorNotFound(Exception):
    pass
