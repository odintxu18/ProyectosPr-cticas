from datetime import datetime, timezone
from src.shared.uow.uow_SQLAlchemy import UnitOfWorkSQLAlchemy
from src.shared.dbmodels.dbmodels import Jugador, Partida, Jugada
from src.juego.repository.jugador_repository import IJugadorRepository


class CrearJugadorUseCase:

    def __init__(self, jugador_repo: IJugadorRepository):
        self.jugador_repo = jugador_repo

    def execute(self, nombre: str, correo: str):
        jugador = Jugador(nombre=nombre, correo=correo)
        self.jugador_repo.add(jugador)


class PartidaJugadaUseCase:
    def crear_partida(self, id_jugador_x: int, id_jugador_o: int):
        with UnitOfWorkSQLAlchemy() as uow:
            nueva_partida = Partida(
                id_jugador_x=id_jugador_x,
                id_jugador_o=id_jugador_o,
                fecha_inicio=datetime.now(timezone.utc),
            )
            uow.partidas_jugadas.agregar_partida(nueva_partida)
            return nueva_partida

    def registrar_jugada(
        self, id_partida: int, id_jugador: int, turno: int, fila: int, columna: int
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

    def finalizar_partida(self, id_partida: int, id_ganador: int = None):
        with UnitOfWorkSQLAlchemy() as uow:
            partida = uow.partidas_jugadas.obtener_partida_por_id(id_partida)
            if not partida:
                raise ValueError("Partida no encontrada")
            partida.id_ganador = id_ganador
            partida.fecha_fin = datetime.now(timezone.utc)
            uow.partidas_jugadas.actualizar_partida(partida)
            return partida

    def obtener_historial_jugadas(self, id_partida: int):
        with UnitOfWorkSQLAlchemy() as uow:
            return uow.partidas_jugadas.obtener_jugadas_por_partida(id_partida)
