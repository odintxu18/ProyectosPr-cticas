from datetime import datetime
from http import client

from pydantic.v1 import validate_email

from src.jugador.applicacion.use_cases import use_cases_jugador

from src.partida.domain.jugada import Jugada
from src.partida.domain.partida import Partida
from src.partida.handler import handler_jugada_partida
from test.common.FakeUnitofWork import FakeUnitOfWork
from ..common.fixtures import *
from src.shared.web.api import app


def test_crear_partida_endpoint(jugador_x, jugador_o):
    validate_email(jugador_x.email)
    validate_email(jugador_o.email)
    response = client.post(
        "/partidas/",
        json={"id_jugador_x": jugador_x.id, "id_jugador_o": jugador_o.id},
    )

    assert response.status_code == 201
    assert response.json()["mensaje"] == "Partida creada correctamente"


def test_registrar_jugada(
    fake_repo_jugadores, fake_repo_partidas, jugador_x, jugador_o, partida
):
    fake_repo_jugadores.add(jugador_x)
    fake_repo_jugadores.add(jugador_o)

    uow = FakeUnitOfWork(fake_repo_jugadores, fake_repo_partidas)
    handler = PartidaHandler(uow)

    handler.crear_partida(jugador_x.id, jugador_o.id)

    handler.registrar_jugada(partida.id, jugador_x.id, 1, 0, 0)

    jugadas = fake_repo_partidas.obtener_jugadas_por_partida(partida.id)
    assert len(jugadas) == 1
    assert uow._committed


def test_terminar_partida(
    fake_repo_jugadores, fake_repo_partidas, jugador_x, jugador_o, partida
):
    fake_repo_jugadores.add(jugador_x)
    fake_repo_jugadores.add(jugador_o)
    fake_repo_partidas.agregar_partida(partida)
    uow = FakeUnitOfWork(fake_repo_jugadores, fake_repo_partidas)
    handler = PartidaHandler(uow)

    resultado = handler.terminar_partida(partida.id, jugador_x.id)

    assert resultado is True
    actualizada = fake_repo_partidas.obtener_partida_por_id(partida.id)
    assert actualizada.fecha_fin is not None
    assert actualizada.id_ganador == jugador_x.id
    assert uow._committed


def test_listar_partidas_de_jugador(
    fake_repo_jugadores, fake_repo_partidas, jugador_x, jugador_o
):
    fake_repo_jugadores.add(jugador_x)
    fake_repo_jugadores.add(jugador_o)
    partida = Partida(
        id="test1",
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    fake_repo_partidas.agregar_partida(partida)

    uow = FakeUnitOfWork(fake_repo_jugadores, fake_repo_partidas)
    handler = PartidaHandler(uow)

    partidas = handler.listar_partidas_de_jugador(jugador_x.id)
    assert len(partidas) >= 1


def test_obtener_jugadas_de_partida(
    fake_repo_jugadores, fake_repo_partidas, jugador_x, jugador_o
):
    fake_repo_jugadores.add(jugador_x)
    fake_repo_jugadores.add(jugador_o)
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    fake_repo_partidas.agregar_partida(partida)
    jugada = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=jugador_x.id,
        turno=1,
        fila=0,
        columna=0,
        fecha_jugada=datetime.now(),
    )

    fake_repo_partidas.agregar_jugada(jugada)

    uow = FakeUnitOfWork(fake_repo_jugadores, fake_repo_partidas)
    handler = PartidaHandler(uow)

    jugadas = handler.obtener_jugadas_de_partida(partida.id)
    assert len(jugadas) == 1
