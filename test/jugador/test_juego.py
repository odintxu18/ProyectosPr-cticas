import pytest

from src.jugador.domain.juego import Juego


@pytest.fixture
def jgame():
    yield Juego()


def test_turno_valido(jgame):
    resultado = jgame.realizar_turno(0, 0)
    assert resultado is True
    assert jgame.tablero.tablero[0][0] == "X"
    assert jgame.obtener_jugador_actual() == "O"
    assert jgame.ha_terminado() is False
    assert jgame.obtener_ganador() is None


def test_cambiar_jugador(jgame):
    jgame.obtener_jugador_actual()
    assert jgame.obtener_jugador_actual() == "X"
    jgame.cambiar_jugador()
    assert jgame.obtener_jugador_actual() == "O"
    jgame.obtener_jugador_actual()
    for i in range(5):
        jgame.cambiar_jugador()
    assert jgame.obtener_jugador_actual() == "X"


def test_juego_no_terminado(jgame):
    jgame.ha_terminado()
    assert jgame.ha_terminado() is False
    jgame.realizar_turno(0, 0)
    jgame.realizar_turno(1, 2)
    jgame.realizar_turno(1, 0)
    jgame.realizar_turno(2, 2)
    jgame.ha_terminado()
    assert jgame.ha_terminado() is False


def test_juego_empate(jgame):
    jgame.ha_terminado()
    assert jgame.ha_terminado() is False
    movimientos = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
        (2, 2),
    ]

    for i, (fila, col) in enumerate(movimientos):
        jgame.realizar_turno(fila, col)
    assert jgame.ha_terminado() is True


def test_juego_ganado(jgame):
    jgame.ha_terminado()
    assert jgame.ha_terminado() is False
    jgame.realizar_turno(0, 0)
    jgame.realizar_turno(1, 0)
    jgame.realizar_turno(0, 1)
    jgame.realizar_turno(1, 1)
    jgame.realizar_turno(0, 2)
    assert jgame.ha_terminado() is True


def test_ganador(jgame):
    assert jgame.obetener_ganador is None
    jgame.realizar_turno(0, 0)
    jgame.realizar_turno(1, 0)
    jgame.realizar_turno(0, 1)
    jgame.realizar_turno(1, 1)
    jgame.realizar_turno(0, 2)
    assert jgame.obtener_ganador() == "X"
    jgame.reiniciar()
    jgame.realizar_turno(0, 0)
    jgame.realizar_turno(1, 0)
    jgame.realizar_turno(2, 0)
    jgame.realizar_turno(1, 1)
    jgame.realizar_turno(0, 2)
    jgame.realizar_turno(1, 2)
    assert jgame.obtener_ganador() == "O"


def test_reiniciar(jgame):
    jgame.realizar_turno(0, 0)
    jgame.realizar_turno(1, 0)
    jgame.realizar_turno(0, 1)
    jgame.reiniciar()
    assert jgame.jugador_actual == "X"
    assert jgame.obtener_ganador() is None
    assert jgame.tablero.esta_lleno() is False
