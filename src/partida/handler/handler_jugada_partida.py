from fastapi import APIRouter

from src.partida.settings.dependencies import partida_dependencies
from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.partida.application.use_cases_jugada_partida import (
    crear_partida,
    registrar_jugada,
    terminar_partida,
    listar_partidas_jugador,
    obtener_jugadas_por_partida,
)

app_partida = APIRouter(prefix="/partidas", tags=["Partidas"])


@router.post("/", status_code=201)
def crear_partida_endpoint(datos_partida: dict):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        crear_partida(
            datos_partida["jugador_x_email"],
            datos_partida["jugador_o_email"],
            uow.get_repository("partida"),
            uow.get_repository("jugador"),
        )

    return {"mensaje": "Partida creada correctamente"}


@router.post("/jugada")
def registrar_jugada_endpoint(datos_jugada: dict):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        registrar_jugada(
            datos_jugada["id_partida"],
            datos_jugada["id_jugador"],
            datos_jugada["turno"],
            datos_jugada["fila"],
            datos_jugada["columna"],
            uow.get_repository("partida"),
        )
    return {"mensaje": "Jugada registrada correctamente"}


@router.post("/terminar")
def terminar_partida_endpoint(datos_partida_terminada: dict):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
        resultado = terminar_partida(
            datos_partida_terminada["id_partida"],
            datos_partida_terminada["id_ganador"],
            partida_repo,
        )
    return {"terminada": resultado}


@router.get("/jugador/{id_jugador}")
def listar_partidas_de_jugador_endpoint(datos_jugador: dict):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
        partidas = listar_partidas_jugador(datos_jugador["id_jugador"], partida_repo)
    return partidas


@router.get("/{id_partida}/jugadas")
def obtener_jugadas_de_partida_endpoint(datos_partida: str):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        jugadas = obtener_jugadas_por_partida(
            datos_partida["id_partida"], uow.get_repository("partida")
        )
    return jugadas
