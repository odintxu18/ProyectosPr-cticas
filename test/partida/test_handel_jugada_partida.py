from src.shared.dbmodels.dbmodels import Jugador, Jugada, Partida
from ..common.fixtures import *
import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.partida.handler.handler_jugada_partida import app_partida


def test_crear_partida_exitosa(session):

    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    jugador_x = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"Nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    jugador_o = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"NOMBRE{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )

    session.add_all([jugador_x, jugador_o])
    session.commit()

    datos_partida = {
        "jugador_x_email": jugador_x.correo,
        "jugador_o_email": jugador_o.correo,
    }

    response = client.post("/partidas/", json=datos_partida)

    assert response.status_code == 201
    data = response.json()
    assert "id_partida" in data

    partida_db = session.query(Partida).filter_by(id=data["id_partida"]).first()
    assert partida_db is not None
    assert partida_db.jugador_x.id == jugador_x.id
    assert partida_db.jugador_o.id == jugador_o.id


def test_registrar_jugada_exitosa(session):
    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    jugador_x = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    jugador_o = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"Nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    session.add_all([jugador_x, jugador_o])
    session.commit()

    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    session.add(partida)
    session.commit()

    datos_jugada = {
        "id_partida": partida.id,
        "id_jugador": jugador_x.id,
        "turno": "X",
        "fila": 0,
        "columna": 0,
    }
    response = client.post("partidas/jugada", json=datos_jugada)

    assert response.status_code == 201
    assert response.json() == {"mensaje": "Jugada registrada correctamente"}


def test_registrar_jugada_jugador_incorrecto(session):
    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    jugador_x = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    session.add(jugador_x)
    session.commit()

    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=str(uuid.uuid4()),
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    session.add(partida)
    session.commit()

    datos_jugada = {
        "id_partida": partida.id,
        "id_jugador": str(uuid.uuid4()),  # jugador desconocido
        "turno": "O",
        "fila": 0,
        "columna": 0,
    }
    response = client.post("/jugada", json=datos_jugada)

    assert response.status_code == 404


@pytest.mark.parametrize("ganador_turno", ["X", "O"])
def test_terminar_partida_exitosa(session, ganador_turno):

    jugador_x = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    jugador_o = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"Nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    session.add_all([jugador_x, jugador_o])
    session.commit()

    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    session.add(partida)
    session.commit()

    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    email_ganador = jugador_x.correo if ganador_turno == "X" else jugador_o.correo
    datos_partida_terminada = {"id_partida": partida.id, "email_ganador": email_ganador}

    response = client.post("partidas/terminar", json=datos_partida_terminada)

    assert response.status_code == 201
    assert "terminada" in response.json()
    assert response.json()["terminada"] == True
    partida_actualizada = session.get(Partida, partida.id)
    session.refresh(partida)
    assert partida_actualizada.fecha_fin is not None
    assert partida_actualizada.id_ganador is not None


def test_listar_partidas_de_jugador(session):

    jugador = Jugador(
        id=str(uuid.uuid4()),
        nombre=f"nombre{uuid.uuid4().hex[:6]}",
        correo=f"{uuid.uuid4().hex[:6]}@test.com",
    )
    session.add(jugador)

    partida1 = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador.id,
        id_jugador_o=str(uuid.uuid4()),
        fecha_inicio=datetime.now(),
    )
    partida2 = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=str(uuid.uuid4()),
        id_jugador_o=jugador.id,
        fecha_inicio=datetime.now(),
    )
    session.add_all([partida1, partida2])
    session.commit()
    session.refresh(jugador)

    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    response = client.get(f"/partidas/jugador/{jugador.correo}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    for partida in data:
        uuid.UUID(partida["id"])


def test_obtener_jugadas_de_partida(session):
    id_jugador_x = str(uuid.uuid4())
    id_jugador_o = str(uuid.uuid4())

    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=id_jugador_x,
        id_jugador_o=id_jugador_o,
        fecha_inicio=datetime.now(),
    )
    session.add(partida)
    session.commit()

    jugada1 = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=id_jugador_x,
        turno=1,
        fila=0,
        columna=0,
    )

    jugada2 = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=id_jugador_o,
        turno=2,
        fila=0,
        columna=1,
    )

    session.add_all([jugada1, jugada2])
    session.commit()

    session.add_all([jugada1, jugada2])
    session.commit()

    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    response = client.get(f"/partidas/{partida.id}/jugadas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for jugada in data:
        assert jugada["id_partida"] == partida.id
        uuid.UUID(jugada["id"])


def test_obtener_jugada_endpoint(session):

    id_jugador_x = str(uuid.uuid4())
    id_jugador_o = str(uuid.uuid4())

    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=id_jugador_x,
        id_jugador_o=id_jugador_o,
        fecha_inicio=datetime.now(),
    )
    session.add(partida)
    session.commit()

    jugada = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=id_jugador_x,
        turno=1,
        fila=0,
        columna=0,
        fecha_jugada=datetime.now(),
    )
    session.add(jugada)
    session.commit()

    app = FastAPI()
    app.include_router(app_partida)
    client = TestClient(app)

    response = client.get(f"/partidas/{jugada.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == jugada.id
    assert data["id_partida"] == partida.id
    assert data["id_jugador"] == jugada.id_jugador
    assert data["fila"] == jugada.fila
    assert data["columna"] == jugada.columna
    assert data["turno"] == jugada.turno
