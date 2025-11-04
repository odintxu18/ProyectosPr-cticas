from fastapi import APIRouter, HTTPException


from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.jugador.settings.dependencies import jugador_dependencies
from src.jugador.repository.jugador_repository import IJugadorRepository
from src.jugador.application.use_cases_jugador import (
    new_player,
    vaidate_email,
    actualiazar_jugador,
    delete_jugador,
)

app_jugador = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@app_jugador.post("/", status_code=201)
def crear_jugador(datos_jugador: dict):

    vaidate_email(datos_jugador["correo"])
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        new_player(datos_jugador["nombre"], datos_jugador["correo"], jugador_repo)
    return {"mensaje": "Jugador creado correctamente"}


@app_jugador.put("/", status_code=200)
def actualizar_jugador(datos_antiguos: dict, datos_nuevos: dict):

    vaidate_email(datos_antiguos["correo"])
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        jugador = jugador_repo.get_jugador_by_email(datos_antiguos["correo"])
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        actualiazar_jugador(
            jugador, datos_nuevos["nombre"], datos_nuevos["correo"], jugador_repo
        )
    return {"mensaje": "Jugador actualizado correctamente"}


@app_jugador.delete("/", status_code=200)
def eliminar_jugador(datos_jugador: dict):

    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        jugador = jugador_repo.get_jugador_by_email(datos_jugador["correo"])
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        delete_jugador(jugador, jugador_repo)
    return {"mensaje": "Jugador eliminado correctamente"}
