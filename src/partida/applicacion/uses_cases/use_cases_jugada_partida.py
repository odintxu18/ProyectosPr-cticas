from datetime import datetime, timezone

from src.partida.domain.jugada import Jugada
from src.partida.domain.partida import Partida
from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy


def crear_partida(id_jugador_x: str, id_jugador_o: str):
    with UnitOfWorkSQLAlchemy() as uow:
        nueva_partida = Partida(
            id_jugador_x=id_jugador_x,
            id_jugador_o=id_jugador_o,
            fecha_inicio=datetime.now(timezone.utc),
        )
        uow.partidas_jugadas.agregar_partida(nueva_partida)
        return nueva_partida


def registrar_jugada(
    id_partida: str, id_jugador: str, turno: int, fila: int, columna: int
):
    with UnitOfWorkSQLAlchemy() as uow:
        jugada = Jugada(
            id_partida=id_partida,
            id_jugador=id_jugador,
            turno=turno,
            fila=fila,
            columna=columna,
            fecha_jugada=datetime.now(timezone.utc),
        )
        uow.partidas_jugadas.agregar_jugada(jugada)
        return jugada


def finalizar_partida(id_partida: str, id_ganador: str = None):
    with UnitOfWorkSQLAlchemy() as uow:
        partida = uow.partidas_jugadas.obtener_partida_por_id(id_partida)
        if not partida:
            raise ValueError("Partida no encontrada")
        partida.id_ganador = id_ganador
        partida.fecha_fin = datetime.now(timezone.utc)
        uow.partidas_jugadas.actualizar_partida(partida)
        return partida


def obtener_historial_jugadas(id_partida: str):
    with UnitOfWorkSQLAlchemy() as uow:
        return uow.partidas_jugadas.obtener_jugadas_por_partida(id_partida)
