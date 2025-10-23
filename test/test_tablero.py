import pytest

import tablero
from tablero import Tablero
@pytest.fixture
def tablr():
    return Tablero()

def test_colocar_en_casilla_vacia(tablr):
    resultado = tablr.colocar(0, 0, "X")
    assert resultado is True
    assert tablr.tablero[0][0] == "X"

def test_colocar_en_casilla_ocupada(tablr):
    tablr.colocar(1, 1, "O")
    resultado = tablr.colocar(1, 1, "X")
    assert resultado is False
    assert tablr.tablero[1][1] == "O"
def test_ganador_en_fila(tablr):
    tablr.tablero[0] = ["X", "X", "X"]
    assert tablr.comprobar_ganador("X") is True

def test_ganador_en_columna(tablr):
    for i in range(3):
        tablr.tablero[i][1] = "O"
    assert tablr.comprobar_ganador("O") is True

def test_ganador_en_diagonal_principal(tablr):
    for i in range(3):
        tablr.tablero[i][i] = "X"
    assert tablr.comprobar_ganador("X") is True

def test_ganador_en_diagonal_invertida(tablr):
    tablr.tablero[0][2] = "O"
    tablr.tablero[1][1] = "O"
    tablr.tablero[2][0] = "O"
    assert tablr.comprobar_ganador("O") is True
class TestNoGanadores:
    def test_sin_ganador_con_parcial_en_fila(self, tablr):
        tablr.tablero[0] = ["X", "X", " "]
        assert tablr.comprobar_ganador("X") is False

    def test_sin_ganador_con_diferentes_jugadores(self, tablr):
        tablr.tablero[0] = ["X", "O", "X"]
        assert tablr.comprobar_ganador("X") is False
        assert tablr.comprobar_ganador("O") is False
class TestTableroLleno:
    def test_tablero_vacio(self, tablr):
        assert tablr.esta_lleno() is False
        assert tablr.tablero[0][0] == " "

    def test_tablero_ocupado(self, tablr):
        for fila in range(3):
            for columna in range(3):
                tablr.tablero[fila][columna] = "x"
        assert tablr.esta_lleno() is True