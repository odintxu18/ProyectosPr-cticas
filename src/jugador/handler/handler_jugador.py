from fastapi import APIRouter, HTTPException


from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.jugador.settings.dependencies import jugador_dependencies
from src.jugador.repository.jugador_repository import IJugadorRepository
from src.jugador.application.use_cases_jugador import (
    new_player,
    actualiazar_jugador,
    delete_jugador,
    InvalidEmailException,
    JugadorNotFound,
)

app_jugador = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@app_jugador.post("/", status_code=201)
def crear_jugador(datos_jugador: dict):
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        try:
            new_player(
                datos_jugador["nombre"],
                datos_jugador["correo"],
                uow.get_repository("jugador"),
            )
        except InvalidEmailException:
            raise HTTPException(status_code=400, detail="Formato de email no valido")
    return {"mensaje": "Jugador creado correctamente"}


@app_jugador.put("/", status_code=200)
def actualizar_jugador(datos_jugador: dict):
    with UnitOfWorkSQLAlchemy(jugador_dependencies) as uow:
        try:
            actualiazar_jugador(datos_jugador, uow.get_repository("jugador"))
        except JugadorNotFound:
            raise HTTPException(status_code=404, detail="Jugador no encotrado")
        except InvalidEmailException:
            raise HTTPException(status_code=400, detail="Formato de email no valido")
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
