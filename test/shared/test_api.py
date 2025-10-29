import pytest
from fastapi.testclient import TestClient
from src.shared.web.api import app, api_juego


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def reinicio():
    api_juego.juego.reiniciar()
    yield
    api_juego.juego.reiniciar()


def test_jugar_casilla_valida(client):
    response = client.post("/jugar", json={"fila": 0, "col": 0})

    assert response.status_code == 200


def test_jugar_casilla_invalida(client):
    response = client.post("/jugar", json={"fila": 3, "col": 0})
    assert response.status_code == 400


def test_body_correcto(client):
    client.post(url="/jugar", json={"fila": 0, "col": 0})
    client.post(url="/jugar", json={"fila": 1, "col": 0})
    client.post(url="/jugar", json={"fila": 0, "col": 1})
    client.post(url="/jugar", json={"fila": 2, "col": 0})
    response = client.post(url="/jugar", json={"fila": 0, "col": 2})
    assert response.status_code == 200
    assert response.text == '"hay un ganador"'


def test_reinicio_tras_terminar(client):
    client.post("/jugar", json={"fila": 0, "col": 0})
    client.post(url="/jugar", json={"fila": 1, "col": 2})
    client.post(url="/jugar", json={"fila": 0, "col": 1})
    client.post(url="/jugar", json={"fila": 2, "col": 1})
    client.post(url="/jugar", json={"fila": 0, "col": 2})
    estado_antes = client.get("/estado").json()
    assert estado_antes["ganador"] == "X"
    assert estado_antes["terminado"] is True
    response = client.post("/jugar", json={"fila": 2, "col": 2})
    assert response.status_code == 200
    estado_despues = client.get("/estado").json()
    assert estado_despues["ganador"] is None
    assert estado_despues["terminado"] is False
    assert estado_despues["tablero"][2][2] == "X"
    assert all(
        cell == " "
        for fila in estado_despues["tablero"]
        for cell in fila
        if cell != "X"
    )


def test_estado_devuelve_tablero_correcto(client):
    response = client.get("/estado")
    assert response.status_code == 200

    data = response.json()
    tablero = data["tablero"]

    assert isinstance(tablero, list)
    assert len(tablero) == 3
    for fila in tablero:
        assert isinstance(fila, list)
        assert len(fila) == 3


def test_get_jugador_actual(client):
    client.post("/jugar", json={"fila": 0, "col": 0})
    estado = client.get("/estado").json()
    assert estado["jugador_actual"] == "O"
    client.post("/jugar", json={"fila": 0, "col": 1})
    estado = client.get("/estado").json()
    assert estado["jugador_actual"] == "X"


def test_ganador_si_hay(client):
    client.post("/jugar", json={"fila": 0, "col": 0})
    client.post(url="/jugar", json={"fila": 1, "col": 2})
    client.post(url="/jugar", json={"fila": 0, "col": 1})
    client.post(url="/jugar", json={"fila": 2, "col": 1})
    client.post(url="/jugar", json={"fila": 0, "col": 2})
    estado = client.get("estado").json()
    assert estado["ganador"] == "X"


def test_juego_termiando(client):
    client.post("/jugar", json={"fila": 0, "col": 0})
    client.post(url="/jugar", json={"fila": 1, "col": 2})
    client.post(url="/jugar", json={"fila": 0, "col": 1})
    client.post(url="/jugar", json={"fila": 2, "col": 1})
    client.post(url="/jugar", json={"fila": 0, "col": 2})
    estado = client.get("/estado").json()
    assert estado["terminado"] is True
