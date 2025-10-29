import uuid

import pytest
from datetime import datetime

from src.juego.repository.sql_alchemy_jugador_repository import (
    JugadorRepositorySQLAlchemy,
)
from src.partida.repository.sql_alchemy_jugada_partida_repository import (
    PartidaJugadaRepositorySQLAlchemy,
)
from src.shared.uow.SQLAlchemy_repositories import RepositoryContainer
from ..common.fixtures import *
from src.shared.dbmodels.dbmodels import (
    Partida as PartidaModel,
    Jugada as JugadaModel,
    Partida,
)


def test_agregar_partida(session):
    id_jugador_1 = str(uuid.uuid4())
    id_jugador_2 = str(uuid.uuid4())
    datos = {
        "id": str(uuid.uuid4()),
        "id_jugador_x": id_jugador_1,
        "id_jugador_o": id_jugador_2,
        "fecha_inicio": datetime.now(),
    }
    repo = PartidaJugadaRepositorySQLAlchemy(session)
    partida = repo.agregar_partida(datos)
    document = session.query(PartidaModel).filter(PartidaModel.id == datos["id"]).all()
    assert document
    assert len(document) == 1
    assert document[0].id == datos["id"]
    assert document[0].id_jugador_x == id_jugador_1
    assert document[0].id_jugador_o == id_jugador_2


def test_obtener_partida(session):
    repo = PartidaJugadaRepositorySQLAlchemy(session)
    id_jugador_1 = str(uuid.uuid4())
    id_jugador_2 = str(uuid.uuid4())
    datos = {
        "id": str(uuid.uuid4()),
        "id_jugador_x": id_jugador_1,
        "id_jugador_o": id_jugador_2,
        "fecha_inicio": datetime.now(),
    }

    partida = repo.agregar_partida(datos)
    document = repo.obtener_partida({"id": datos["id"]})
    assert document is not None
    assert document["id"] == datos["id"]
    assert document["id_ganador"] is None


def test_obtener_multiples_partidas(session):
    repo = PartidaJugadaRepositorySQLAlchemy(session)

    partidas_data = []
    for _ in range(3):
        datos = {
            "id": str(uuid.uuid4()),
            "id_jugador_x": str(uuid.uuid4()),
            "id_jugador_o": str(uuid.uuid4()),
            "fecha_inicio": datetime.now(),
        }
        repo.agregar_partida(datos)
        partidas_data.append(datos)

    for datos in partidas_data:
        partida = repo.obtener_partida({"id": datos["id"]})
        assert partida is not None
        assert partida["id_jugador_x"] == datos["id_jugador_x"]
        assert partida["id_jugador_o"] == datos["id_jugador_o"]

    todas = repo.listar_partidas({})
    assert len(todas) >= 3

    ids_en_db = {p["id"] for p in todas}
    for datos in partidas_data:
        assert datos["id"] in ids_en_db


def test_actualizar_partida(session):
    repo = PartidaJugadaRepositorySQLAlchemy(session)

    id_jugador_1 = str(uuid.uuid4())
    id_jugador_2 = str(uuid.uuid4())
    id_partida = str(uuid.uuid4())

    datos = {
        "id": id_partida,
        "id_jugador_x": id_jugador_1,
        "id_jugador_o": id_jugador_2,
        "fecha_inicio": datetime.now(),
    }

    repo.agregar_partida(datos)

    datos_act = {
        "fecha_fin": datetime.now(),
        "id_ganador": id_jugador_1,
    }

    actualizado = repo.actualizar_partida({"id": id_partida}, datos_act)
    assert actualizado is True

    partida = repo.obtener_partida({"id_jugador_x": id_jugador_1})
    assert partida is not None
    assert partida["id_ganador"] == id_jugador_1


def test_agregar_jugada(session):
    repo = PartidaJugadaRepositorySQLAlchemy(session)

    id_jugador_1 = str(uuid.uuid4())
    id_jugador_2 = str(uuid.uuid4())
    id_partida = str(uuid.uuid4())

    datos_partida = {
        "id": id_partida,
        "id_jugador_x": id_jugador_1,
        "id_jugador_o": id_jugador_2,
        "fecha_inicio": datetime.now(),
    }
    partida = repo.agregar_partida(datos_partida)

    datos_jugada = {
        "id": str(uuid.uuid4()),
        "id_partida": id_partida,
        "id_jugador": id_jugador_1,
        "turno": 1,
        "fila": 0,
        "columna": 2,
        "fecha_jugada": datetime.now(),
    }

    jugada = repo.agregar_jugada(datos_jugada)

    assert jugada["id"] == datos_jugada["id"]
    assert jugada["id_partida"] == id_partida
    assert jugada["id_jugador"] == id_jugador_1
    assert jugada["fila"] == 0
    assert jugada["columna"] == 2
    assert isinstance(jugada["fecha_jugada"], datetime)


def test_eliminar_jugada(session):
    repo = PartidaJugadaRepositorySQLAlchemy(session)
    id_jugador_1 = str(uuid.uuid4())
    id_jugador_2 = str(uuid.uuid4())
    datos = {
        "id": str(uuid.uuid4()),
        "id_jugador_x": id_jugador_1,
        "id_jugador_o": id_jugador_2,
        "fecha_inicio": datetime.now(),
    }
    partida = repo.agregar_partida(datos)
    datos_jugada = {
        "id_partida": 1,
        "id_jugador": 1,
        "turno": 1,
        "fila": 0,
        "columna": 2,
        "fecha_jugada": datetime.now(),
    }
    jugada = repo.eliminar_jugada(datos_jugada)
    assert jugada is False


def test_add_jugador(session):
    repo = JugadorRepositorySQLAlchemy(session)
    nombre_jugador = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_jugador = f"Correo_{uuid.uuid4().hex[:6]}"
    datos = {
        "id": str(uuid.uuid4()),
        "nombre": nombre_jugador,
        "correo": correo_jugador,
    }

    jugador = repo.add(datos)

    assert jugador["id"] == datos["id"]
    assert jugador["nombre"] == datos["nombre"]
    assert jugador["correo"] == datos["correo"]


def test_get_by_id(session):
    repo = JugadorRepositorySQLAlchemy(session)
    nombre_jugador = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_jugador = f"Correo_{uuid.uuid4().hex[:6]}"
    datos = {
        "id": str(uuid.uuid4()),
        "nombre": nombre_jugador,
        "correo": correo_jugador,
    }

    jugador = repo.add(datos)

    jugador = repo.get_by_id({"id": jugador["id"]})
    assert jugador is not None
    assert jugador["nombre"] == datos["nombre"]
    assert jugador["id"] == datos["id"]


def test_get_by_nombre(session):
    repo = JugadorRepositorySQLAlchemy(session)
    nombre_jugador = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_jugador = f"Correo_{uuid.uuid4().hex[:6]}"
    datos = {
        "id": str(uuid.uuid4()),
        "nombre": nombre_jugador,
        "correo": correo_jugador,
    }

    jugador = repo.add(datos)

    jugador = repo.get_by_id({"nombre": jugador["nombre"]})
    assert jugador is not None
    assert jugador["nombre"] == datos["nombre"]
    assert jugador["id"] == datos["id"]


def test_get_all(session):
    repo = JugadorRepositorySQLAlchemy(session)
    jugadores_data = []
    for _ in range(3):
        datos = {
            "id": str(uuid.uuid4()),
            "nombre": f"Carlos_{uuid.uuid4().hex[:6]}",
            "correo": f"Correo_{uuid.uuid4().hex[:6]}",
        }
        repo.add(datos)
        jugadores_data.append(datos)

    for datos in jugadores_data:
        jugador = repo.get_by_id({"id": datos["id"]})
        assert jugador is not None
        assert jugador["nombre"] == datos["nombre"]
        assert jugador["correo"] == datos["correo"]

    todas = repo.get_all({})
    assert len(todas) >= 3


def test_update_jugador(session):
    repo = JugadorRepositorySQLAlchemy(session)
    nombre_jugador = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_jugador = f"Correo_{uuid.uuid4().hex[:6]}"
    correo_actualizar = f"19Carlstr{(uuid.uuid4()).hex[:6]}"
    datos = {
        "id": str(uuid.uuid4()),
        "nombre": nombre_jugador,
        "correo": correo_jugador,
    }

    jugador = repo.add(datos)
    actualizado = repo.update({"id": jugador["id"]}, {"correo": correo_actualizar})
    assert actualizado is True

    jugador = repo.get_by_id({"id": jugador["id"]})
    assert jugador["correo"] == correo_actualizar


def test_delete_jugador(session):
    repo = JugadorRepositorySQLAlchemy(session)
    nombre_jugador = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_jugador = f"Correo_{uuid.uuid4().hex[:6]}"
    datos = {
        "id": str(uuid.uuid4()),
        "nombre": nombre_jugador,
        "correo": correo_jugador,
    }
    jugador = repo.add(datos)

    eliminado = repo.delete({"id": jugador["id"]})
    assert eliminado is True

    jugador = repo.get_by_id({"id": jugador["id"]})
    assert jugador is None
