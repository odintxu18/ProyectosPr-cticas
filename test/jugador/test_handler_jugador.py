from src.juego.handler.handler_jugador import JugadorHandler
from test.common.FakeUnitofWork import FakeUnitOfWork
from ..common.fixtures import *
from src.juego.domain.jugador import Jugador


def test_crear_jugador(fake_repo_jugadores, nombre, correo):
    uow = FakeUnitOfWork(fake_repo_jugadores)
    handler = JugadorHandler(uow)

    handler.crear_jugador(nombre, correo)

    assert uow._committed is True


def test_actualizar_jugador(fake_repo_jugadores, jugador_x):
    fake_repo_jugadores.add(jugador_x)
    uow = FakeUnitOfWork(fake_repo_jugadores)
    handler = JugadorHandler(uow)

    nuevo_nombre = f"NuevoNombre_{uuid.uuid4().hex[:6]}"
    nuevo_correo = f"nuevo_{uuid.uuid4().hex[:6]}@correo.com"
    handler.actualizar_jugador(jugador_x.id, nuevo_nombre, nuevo_correo)

    actualizado = fake_repo_jugadores.get_by_id(jugador_x.id)
    assert actualizado.nombre == nuevo_nombre
    assert actualizado.correo == nuevo_correo
    assert uow._committed


def test_eliminar_jugador(fake_repo_jugadores, jugador_x):
    fake_repo_jugadores.add(jugador_x)
    uow = FakeUnitOfWork(fake_repo_jugadores)
    handler = JugadorHandler(uow)

    handler.eliminar_jugador(jugador_x.id)

    assert uow._committed
