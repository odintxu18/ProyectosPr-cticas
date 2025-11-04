from sqlite3 import IntegrityError

import logging
from fastapi import APIRouter, HTTPException

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

router = APIRouter(prefix="/partidas", tags=["Partidas"])


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
def registrar_jugada_endpoint(jugada: JugadaCreate):

    try:
        with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
            registrar_jugada(
                jugada.id_partida,
                jugada.id_jugador,
                jugada.turno,
                jugada.fila,
                jugada.columna,
                uow.get_repository("partida"),
            )
        return {"mensaje": "Jugada registrada correctamente"}
    except Exception as e:
        raise manejar_error(e, "registrar_partida")


@router.post("/terminar")
def terminar_partida_endpoint(data: TerminarPartida):

    try:
        with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            resultado = terminar_partida(data.id_partida, data.id_ganador, partida_repo)
        return {"terminada": resultado}
    except Exception as e:
        raise manejar_error(e, "terminar_partida")


@router.get("/jugador/{id_jugador}")
def listar_partidas_de_jugador_endpoint(id_jugador: str):

    try:
        with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
            partida_repo: IPartidaJugadaRepository = uow.get_repository("partida")
            partidas = listar_partidas_jugador(id_jugador, partida_repo)
        return partidas
    except Exception as e:
        raise manejar_error(e, "listar_partidas")


@router.get("/{id_partida}/jugadas")
def obtener_jugadas_de_partida_endpoint(id_partida: str):

    with UnitOfWorkSQLAlchemy(partida_dependencies) as uow:
        jugadas = obtener_jugadas_por_partida(id_partida, uow.get_repository("partida"))
    return jugadas
