from fastapi import FastAPI


from src.jugador.handler.handler_jugador import app_jugador

from src.shared.dbmodels.dbmodels import Jugador
from ..common.fixtures import *

from fastapi.testclient import TestClient


def test_crear_jugador_exitoso(session):
    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)
    datos = {
        "nombre": str(uuid.uuid4().hex[:6]),
        "correo": f"Correo_{uuid.uuid4().hex[:6]}@testing.com",
    }
    response = client.post("jugadores", json=datos)
    aka = session.query(Jugador).filter_by(nombre="nombre").first()
    assert response.status_code == 201


def test_crear_jugador_email_invalido(session):
    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)
    datos = {"nombre": "Carlos", "correo": "correo_invalido"}

    response = client.post("/jugadores/", json=datos)
    aka = session.query(Jugador).filter_by(nombre="nombre").first()
    assert response.status_code == 400
    assert response.json()["detail"] == "Formato de email no valido"


def test_get_jugador_exitoso(session):

    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)

    id_unico = f"id_{uuid.uuid4().hex[:6]}@testing.com"
    nombre_unico = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_unico = f"Correo_{uuid.uuid4().hex[:6]}@testing.com"
    jugador = Jugador(id=id_unico, nombre=nombre_unico, correo=correo_unico)
    session.add(jugador)
    session.commit()

    response = client.get(f"/jugadores/jugador/{jugador.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nombre_unico
    assert data["correo"] == correo_unico


def test_get_jugador_no_encontrado(session):
    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)

    response = client.get("/jugadores/jugador/9999")

    assert response.status_code == 500


def test_delete_jugador_exitoso(session):

    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)

    id_unico = str(uuid.uuid4())
    nombre_unico = f"Carlos_{uuid.uuid4().hex[:6]}"
    correo_unico = f"{uuid.uuid4().hex[:6]}@test.com"

    jugador = Jugador(id=id_unico, nombre=nombre_unico, correo=correo_unico)
    session.add(jugador)
    session.commit()

    response = client.request(
        "DELETE",
        f"/jugadores",
        json={"id": id_unico, "nombre": nombre_unico, "correo": correo_unico},
    )

    assert response.status_code in (200, 204)
    assert "mensaje" in response.json()
    assert response.json()["mensaje"] == "Jugador eliminado correctamente"

    jugador_db = session.query(Jugador).filter_by(id=id_unico).first()
    assert jugador_db is None


def test_actualizar_jugador_exitoso(session):

    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)

    id_unico = str(uuid.uuid4())
    jugador = Jugador(
        id=id_unico,
        nombre=f"Carlos_{uuid.uuid4().hex[:6]}",
        correo=f"Correo{uuid.uuid4().hex[:6]}@test.com",
    )
    session.add(jugador)
    session.commit()

    datos_actualizados = {
        "id": id_unico,
        "nombre": f"Carlos_Nuevo_{uuid.uuid4().hex[:6]}",
        "correo": f"Correo_Muevo{uuid.uuid4().hex[:6]}@testing.com",
    }

    response = client.put("/jugadores/", json=datos_actualizados)

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Jugador actualizado correctamente"

    jugador_actualizado = session.query(Jugador).filter_by(id=id_unico).first()
    assert jugador_actualizado.nombre == datos_actualizados["nombre"]
    assert jugador_actualizado.correo == datos_actualizados["correo"]


def test_actualizar_jugador_no_encontrado(session):

    app = FastAPI()
    app.include_router(app_jugador)
    client = TestClient(app)

    datos_inexistentes = {
        "id": str(uuid.uuid4()),
        "nombre": "Fantasma",
        "correo": "fantasma@test.com",
    }

    response = client.put("/jugadores/", json=datos_inexistentes)

    assert response.status_code == 404
    assert response.json()["detail"] == "Jugador no encotrado"
