import re
import uuid
from datetime import datetime

from src.juego.domain.jugador import Jugador
from src.partida.applicacion.uses_cases.use_cases_jugada_partida import (
    registrar_jugada,
    crear_partida,
    terminar_partida,
    listar_partidas_jugador,
    obtener_jugadas_por_partida,
)
from ..common.fixtures import *
from src.partida.domain.partida import Partida
from src.partida.domain.jugada import Jugada


def test_crear_partida(jugador_x: Jugador, jugador_o: Jugador, fake_repo_partidas):
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=uuid.uuid4().hex,
    )
    fake_repo_partidas.agregar_partida(partida)
    assert partida.id_jugador_x == jugador_x.id


def test_registrar_jugada_guarda_jugada(fake_repo_partidas, jugador_x, jugador_o):
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    fake_repo_partidas.agregar_partida(partida)

    registrar_jugada(
        id_partida=partida.id,
        id_jugador=jugador_x.id,
        turno=1,
        fila=0,
        columna=1,
        repo_jugada=fake_repo_partidas,
    )

    jugadas = fake_repo_partidas.obtener_jugadas_por_partida(partida.id)
    assert len(jugadas) == 1
    j = jugadas[0]
    assert j.id_partida == partida.id
    assert j.id_jugador == jugador_x.id
    assert j.turno == 1
    assert j.fila == 0
    assert j.columna == 1


def test_terminar_partida_actualiza_fecha_y_ganador(
    fake_repo_partidas, jugador_x, jugador_o
):
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    fake_repo_partidas.agregar_partida(partida)

    exito = terminar_partida(partida.id, jugador_x.id, fake_repo_partidas)
    assert exito is True

    actualizada = fake_repo_partidas.obtener_partida_por_id(partida.id)
    assert actualizada.id_ganador == jugador_x.id
    assert actualizada.fecha_fin is not None


def test_listar_partidas_jugador_retorna_solo_las_del_jugador(
    fake_repo_partidas, jugador_x, jugador_o
):
    partida_1 = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    partida_2 = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x="otro_id",
        id_jugador_o="otro_id2",
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )

    fake_repo_partidas.agregar_partida(partida_1)
    fake_repo_partidas.agregar_partida(partida_2)

    result = listar_partidas_jugador(jugador_x.id, fake_repo_partidas)
    assert len(result) == 1
    assert result[0].id == partida_1.id


def test_obtener_jugadas_por_partida_devuelve_correctas(
    fake_repo_partidas, jugador_x, jugador_o
):
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    fake_repo_partidas.agregar_partida(partida)

    jugada_1 = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=jugador_x.id,
        turno=1,
        fila=0,
        columna=0,
        fecha_jugada=datetime.now(),
    )
    fake_repo_partidas.agregar_jugada(jugada_1)

    jugadas = obtener_jugadas_por_partida(partida.id, fake_repo_partidas)
    assert len(jugadas) == 1
    assert jugadas[0].id == jugada_1.id
    assert jugadas[0].id_partida == partida.id
