from sqlite3 import IntegrityError

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.shared.uow.SQLAlchemy_repositories import RepositoryContainer
from src.juego.repository.jugador_repository import IJugadorRepository
from src.juego.applicacion.use_cases.use_cases_jugador import (
    new_player,
    vaidate_email,
    actualiazar_jugador,
    delete_jugador,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


class JugadorCreate(BaseModel):
    nombre: str
    correo: EmailStr


class JugadorUpdate(BaseModel):
    nombre: str
    correo: EmailStr


def manejar_error(e: Exception, contexto: str = ""):

    logger.error(f"[{contexto}] Error: {e}")

    if isinstance(e, HTTPException):
        raise e
    elif isinstance(e, IntegrityError):
        raise HTTPException(status_code=409, detail=f"Conflicto de datos ({contexto})")

    elif isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e))
    elif isinstance(e, KeyError):
        raise HTTPException(
            status_code=404, detail=f"Recurso no encontrado ({contexto})"
        )
    else:
        raise HTTPException(
            status_code=500, detail=f"Error inesperado: {str(e) or 'Desconocido'}"
        )


@router.post("/", status_code=201)
def crear_jugador(jugador: JugadorCreate):

    try:
        vaidate_email(jugador.correo)
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            jugador_repo: IJugadorRepository = uow.get_repository("jugador")
            new_player(jugador.nombre, jugador.correo, jugador_repo)
        return {"mensaje": "Jugador creado correctamente"}
    except Exception as e:
        manejar_error(e, "crear_jugador")


@router.put("/{jugador_id}")
def actualizar_jugador(jugador_id: str, datos: JugadorUpdate):

    try:
        vaidate_email(datos.correo)
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            jugador_repo: IJugadorRepository = uow.get_repository("jugador")
            jugador = jugador_repo.get_by_id(jugador_id)
            if not jugador:
                raise HTTPException(status_code=404, detail="Jugador no encontrado")
            actualiazar_jugador(jugador, datos.nombre, datos.correo, jugador_repo)
        return {"mensaje": "Jugador actualizado correctamente"}
    except Exception as e:
        manejar_error(e, "actualizar_jugador")


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: str):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            jugador_repo: IJugadorRepository = uow.get_repository("jugador")
            jugador = jugador_repo.get_by_id(jugador_id)
            if not jugador:
                raise HTTPException(status_code=404, detail="Jugador no encontrado")
            delete_jugador(jugador, jugador_repo)
        return {"mensaje": "Jugador eliminado correctamente"}
    except Exception as e:
        manejar_error(e, "eliminar_jugador")
