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

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@router.post("/", status_code=201)
def crear_jugador(datos_jugador: dict):

    vaidate_email(datos_jugador["correo"])
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        new_player(datos_jugador["nombre"], datos_jugador["correo"], jugador_repo)
    return {"mensaje": "Jugador creado correctamente"}


@router.put("/{jugador_id}")
def actualizar_jugador(datos_antiguos: dict, datos_nuevos: dict):

    vaidate_email(datos_antiguos["correo"])
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        jugador = jugador_repo.get_jugador_by_email(datos_antiguos["email"])
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        actualiazar_jugador(
            jugador, datos_nuevos["nombre"], datos_nuevos["correo"], jugador_repo
        )
    return {"mensaje": "Jugador actualizado correctamente"}


@router.delete("/{jugador_id}")
def eliminar_jugador(datos_jugador: dict):

    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        jugador_repo: IJugadorRepository = uow.get_repository("jugador")
        jugador = jugador_repo.get_jugador_by_email(datos_jugador["email"])
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        delete_jugador(jugador, jugador_repo)
    return {"mensaje": "Jugador eliminado correctamente"}
