import uuid


from datetime import datetime


from ..common.fixtures import *
from src.shared.dbmodels.dbmodels import *


def test_agregar_partida(repo_partidas, partida):
    partida_guardada = repo_partidas.agregar_partida(partida)
    assert partida_guardada.id == partida.id
    assert partida_guardada.id_jugador_x == partida.id_jugador_x
    assert partida_guardada.id_jugador_o == partida.id_jugador_o


def test_obtener_partida(repo_partidas, partida):
    repo_partidas.agregar_partida(partida)
    partida_db = repo_partidas.obtener_partida_por_id(partida.id)
    assert partida_db.id == partida.id


def test_obtener_multiples_partidas(repo_partidas, partida):
    repo_partidas.agregar_partida(partida)
    partidas = repo_partidas.listar_partidas()
    assert len(partidas) >= 1
    assert any(p.id == partida.id for p in partidas)


def test_actualizar_partida(repo_partidas, partida):
    repo_partidas.agregar_partida(partida)
    nuevo_ganador = f"nuevo_{uuid.uuid4().hex[:6]}"
    partida.id_ganador = nuevo_ganador
    actualizado = repo_partidas.actualizar_partida(partida)
    assert actualizado is True
    partida_act = repo_partidas.obtener_partida_por_id(partida.id)
    assert partida_act.id_ganador == nuevo_ganador


def test_borrar_partida(repo_partidas, partida):
    repo_partidas.agregar_partida(partida)
    eliminado = repo_partidas.delete_partida(partida.id)
    assert eliminado is True
    part_eli = repo_partidas.obtener_partida_por_id(partida.id)
    assert part_eli is None


def test_agregar_jugada(repo_partidas, jugada):
    jugada_guarda = repo_partidas.agregar_jugada(jugada)
    assert jugada_guarda.id == jugada.id


def test_eliminar_jugada(repo_partidas, jugada):
    jugada_guarda = repo_partidas.agregar_jugada(jugada)
    eliminada = repo_partidas.eliminar_jugada(jugada.id)
    assert eliminada is True
    jugada_eli = repo_partidas.obtener_jugada_por_id(jugada.id)
    assert jugada_eli is None


def test_buscar_jugada(repo_partidas, jugada):
    repo_partidas.agregar_jugada(jugada)
    jugada_db = repo_partidas.obtener_jugada_por_id(jugada.id)
    assert jugada_db.id == jugada.id


def test_obtener_jugadas_por_partida(repo_partidas, partida, jugada):

    repo_partidas.session.add(jugada)
    repo_partidas.session.commit()

    resultado = repo_partidas.obtener_jugadas_por_partida(partida.id)

    assert len(resultado) == 1
    jugada_resultado: Jugada = resultado[0]
    assert jugada_resultado.id == jugada.id
    assert jugada_resultado.id_partida == partida.id
    assert jugada_resultado.id_jugador == jugada.id_jugador
    assert jugada_resultado.turno == jugada.turno
    assert jugada_resultado.fila == jugada.fila
    assert jugada_resultado.columna == jugada.columna
    assert jugada.fecha_jugada == jugada_resultado.fecha_jugada


def test_obtener_jugadas_por_partida_varias(
    repo_partidas, partida, jugador_x, jugador_o
):

    jugada1 = jugada_mother(partida, jugador_x, turno=2, fila=0, columna=1)
    jugada2 = jugada_mother(partida, jugador_o, turno=1, fila=1, columna=0)
    repo_partidas.session.add_all([jugada1, jugada2])
    repo_partidas.session.commit()

    resultado = repo_partidas.obtener_jugadas_por_partida(partida.id)

    assert len(resultado) == 2
    assert resultado[0].turno == 1
    assert resultado[1].turno == 2


def test_add_jugador(repo_jugadores, jugador_x):
    jugador_guardado = repo_jugadores.add(jugador_x)
    assert jugador_guardado.id == jugador_x.id
    assert jugador_guardado.nombre == jugador_x.nombre


def test_get_by_id(repo_jugadores, jugador_x):
    repo_jugadores.add(jugador_x)
    jugador_db = repo_jugadores.get_by_id(jugador_x.id)
    assert jugador_db.id == jugador_x.id
    assert jugador_db.nombre == jugador_x.nombre


def test_get_all(repo_jugadores, jugador_x):
    repo_jugadores.add(jugador_x)
    jugadores = repo_jugadores.get_all()
    assert len(jugadores) >= 1
    assert any(j.id == jugador_x.id for j in jugadores)


def test_update_jugador(repo_jugadores, jugador_x):
    repo_jugadores.add(jugador_x)
    nuevo_correo = f"nuevo_{uuid.uuid4().hex[:6]}"
    jugador_x.correo = nuevo_correo
    actualizado = repo_jugadores.update(jugador_x)
    assert actualizado is True
    jugador_act = repo_jugadores.get_by_id(jugador_x.id)
    assert jugador_act.correo == nuevo_correo


def test_delete_jugador(repo_jugadores, jugador_x):
    repo_jugadores.add(jugador_x)
    eliminado = repo_jugadores.delete(jugador_x.id)
    assert eliminado is True
    jug_eli = repo_jugadores.get_by_id(jugador_x.id)
    assert jug_eli is None
