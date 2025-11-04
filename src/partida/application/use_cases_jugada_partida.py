import uuid
from datetime import datetime, timezone

from src.partida.repository.jugador_repository import IJugadorRepository
from src.partida.domain.jugada import Jugada
from src.partida.domain.partida import Partida
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository


def crear_partida(
    jugador_x_email: str,
    jugador_o_email: str,
    repo_partida: IPartidaJugadaRepository,
    repo_jugador: IJugadorRepository,
):

    jugador_x = repo_jugador.get_jugador_by_email(jugador_x_email)
    jugador_o = repo_jugador.get_jugador_by_email(jugador_o_email)
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=None,
    )
    repo_partida.agregar_partida(partida)


def registrar_jugada(
    id_partida: str,
    id_jugador: str,
    turno: int,
    fila: int,
    columna: int,
    repo_jugada: IPartidaJugadaRepository,
):

    jugada = Jugada(
        id=str(uuid.uuid4()),
        id_partida=id_partida,
        id_jugador=id_jugador,
        turno=turno,
        fila=fila,
        columna=columna,
        fecha_jugada=datetime.now(timezone.utc),
    )

    repo_jugada.agregar_jugada(jugada)


def terminar_partida(
    id_partida: str, id_ganador: str, repo_partida: IPartidaJugadaRepository
):

    partida = repo_partida.obtener_partida_por_id(id_partida)
    if not partida:
        return False

    if partida.fecha_fin is not None:
        return False

    partida.id_ganador = id_ganador
    partida.fecha_fin = datetime.now()

    actualizado = repo_partida.actualizar_partida(partida)
    return actualizado


def listar_partidas_jugador(
    id_jugador: str,
    repo_partida: IPartidaJugadaRepository,
):
    partidas = repo_partida.listar_partidas()
    return [
        Partida(
            id=p.id,
            id_jugador_x=p.id_jugador_x,
            id_jugador_o=p.id_jugador_o,
            fecha_inicio=p.fecha_inicio,
            fecha_fin=p.fecha_fin,
            id_ganador=p.id_ganador,
        )
        for p in partidas
        if p.id_jugador_x == id_jugador or p.id_jugador_o == id_jugador
    ]


def obtener_jugadas_por_partida(id_partida: str, repo_jugada: IPartidaJugadaRepository):
    jugadas = repo_jugada.obtener_jugadas_por_partida(id_partida)
    return [
        Jugada(
            id=j.id,
            id_partida=j.id_partida,
            id_jugador=j.id_jugador,
            turno=j.turno,
            fila=j.fila,
            columna=j.columna,
            fecha_jugada=j.fecha_jugada,
        )
        for j in jugadas
        if j.id_partida == id_partida
    ]
