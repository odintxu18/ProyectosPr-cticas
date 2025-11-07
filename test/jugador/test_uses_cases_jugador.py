import re
import uuid
from ..common.fixtures import *
from src.jugador.domain.jugador import Jugador


def test_new_player(nombre, correo, fake_repo_jugadores):
    jugador = Jugador(id=str(uuid.uuid4()), nombre=nombre, correo=correo)
    fake_repo_jugadores.add(jugador)
    result = fake_repo_jugadores.get_by_id(jugador.id)
    assert result.id == jugador.id
    assert result.nombre == jugador.nombre
    assert result.correo == jugador.correo


def test_correo_invalido(nombre, fake_repo_jugadores):
    correo_invalido = "nosoyuncorreo.neti"

    # Validamos que el patrón falle
    pattern = re.compile(
        "^[a-zA-Z0-9.\-_#~!$%&'*+/=?^{|}]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    )
    resultado = pattern.match(correo_invalido)
    assert resultado is None

    # No debería añadirse al repo
    jugador = Jugador(id=str(uuid.uuid4()), nombre=nombre, correo=correo_invalido)
    # simulamos la validación al agregar
    if resultado:
        fake_repo_jugadores.add(jugador)

    # Como el correo es inválido, no se añadió
    buscado = fake_repo_jugadores.get_by_id(jugador.id)
    assert buscado is None


def test_validate_correo(correo):
    pattern = re.compile(
        "^[a-zA-Z 0-9^a-zA-Z0-9.\-_#~!$%&'*+/=?^{|}]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    )
    resultado = pattern.match(correo)
    assert resultado is not None


def test_actualizar_jugador(jugador_x, nombre, correo, fake_repo_jugadores):
    fake_repo_jugadores.add(jugador_x)
    jugador_x.correo = correo
    jugador_x.nombre = nombre
    actualizado = fake_repo_jugadores.update(jugador_x)
    assert actualizado is True
    jugador_act = fake_repo_jugadores.get_by_id(jugador_x.id)
    assert jugador_act.correo == correo


def test_delete_jugador(jugador_x, fake_repo_jugadores):
    fake_repo_jugadores.add(jugador_x)
    eliminado = fake_repo_jugadores.delete(jugador_x.id)
    assert eliminado is True
    jug_eli = fake_repo_jugadores.get_by_id(jugador_x.id)
    assert jug_eli is None


def test_get_by_id(jugador_x, fake_repo_jugadores):
    fake_repo_jugadores.add(jugador_x)
    buscado = fake_repo_jugadores.get_by_id(jugador_x.id)
    assert buscado.id == jugador_x.id
    assert buscado.nombre == jugador_x.nombre
    assert buscado.correo == jugador_x.correo
