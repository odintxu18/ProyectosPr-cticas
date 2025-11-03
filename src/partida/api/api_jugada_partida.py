from sqlite3 import IntegrityError

from _pytest import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.shared.uow.SQLAlchemy_repositories import RepositoryContainer
from src.juego.repository.jugador_repository import IJugadorRepository
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.partida.applicacion.uses_cases.use_cases_jugada_partida import (
    crear_partida,
    registrar_jugada,
    terminar_partida,
    listar_partidas_jugador,
    obtener_jugadas_por_partida,
)

router = APIRouter(prefix="/partidas", tags=["Partidas"])

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PartidaCreate(BaseModel):
    id_jugador_x: str
    id_jugador_o: str


class JugadaCreate(BaseModel):
    id_partida: str
    id_jugador: str
    turno: int
    fila: int
    columna: int


class TerminarPartida(BaseModel):
    id_partida: str
    id_ganador: str


def manejar_error(e: Exception, contexto: str = ""):
    """Centraliza el manejo de errores."""
    logger.error(f"[{contexto}] Error: {e}")

    if isinstance(e, HTTPException):
        raise e

    elif isinstance(e, IntegrityError):
        raise HTTPException(
            status_code=409,
            detail=f"Conflicto de integridad en base de datos ({contexto})",
        )

    elif isinstance(e, SQLAlchemyError):
        raise HTTPException(
            status_code=500,
            detail=f"Error interno de base de datos ({contexto})",
        )

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
def crear_partida_endpoint(datos: PartidaCreate):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            jugador_repo: IJugadorRepository = uow.get_repository("jugador")
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")

            jugador_x = jugador_repo.get_by_id(datos.id_jugador_x)
            jugador_o = jugador_repo.get_by_id(datos.id_jugador_o)

            if not jugador_x or not jugador_o:
                raise HTTPException(status_code=400, detail="Jugadores no válidos")

            crear_partida(jugador_x, jugador_o, partida_repo)

        return {"mensaje": "Partida creada correctamente"}
    except Exception as e:
        raise manejar_error(e, "crear_partida")


@router.post("/jugada")
def registrar_jugada_endpoint(jugada: JugadaCreate):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            registrar_jugada(
                jugada.id_partida,
                jugada.id_jugador,
                jugada.turno,
                jugada.fila,
                jugada.columna,
                partida_repo,
            )
        return {"mensaje": "Jugada registrada correctamente"}
    except Exception as e:
        raise manejar_error(e, "registrar_partida")


@router.post("/terminar")
def terminar_partida_endpoint(data: TerminarPartida):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            resultado = terminar_partida(data.id_partida, data.id_ganador, partida_repo)
        return {"terminada": resultado}
    except Exception as e:
        raise manejar_error(e, "terminar_partida")


@router.get("/jugador/{id_jugador}")
def listar_partidas_de_jugador_endpoint(id_jugador: str):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            partidas = listar_partidas_jugador(id_jugador, partida_repo)
        return partidas
    except Exception as e:
        raise manejar_error(e, "listar_partidas")


@router.get("/{id_partida}/jugadas")
def obtener_jugadas_de_partida_endpoint(id_partida: str):

    try:
        with UnitOfWorkSQLAlchemy(RepositoryContainer) as uow:
            jugada_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            jugadas = obtener_jugadas_por_partida(id_partida, jugada_repo)
        return jugadas
    except Exception as e:
        raise manejar_error(e, "obtener_jugada")
