from src.partida.applicacion.uses_cases.use_cases_jugada_partida import (
    crear_partida,
    registrar_jugada,
    terminar_partida,
    listar_partidas_jugador,
    obtener_jugadas_por_partida,
)
from src.juego.repository.jugador_repository import IJugadorRepository
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.shared.uow.unit_of_work import IUnitOfWork


class PartidaHandler:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def crear_partida(self, id_jugador_x: str, id_jugador_o: str):
        jugador_repo: IJugadorRepository = self.uow.get_repository("jugador")
        repo_partida: IPartidaJugadaRepository = self.uow.get_repository("partida")

        jugador_x = jugador_repo.get_by_id(id_jugador_x)
        jugador_o = jugador_repo.get_by_id(id_jugador_o)
        if not jugador_x or not jugador_o:
            raise Exception("Jugadores no válidos")

        crear_partida(jugador_x, jugador_o, repo_partida)
        self.uow.commit()

    def registrar_jugada(
        self, id_partida: str, id_jugador: str, turno: int, fila: int, columna: int
    ):
        repo_jugada: IPartidaJugadaRepository = self.uow.get_repository("jugada")
        registrar_jugada(id_partida, id_jugador, turno, fila, columna, repo_jugada)
        self.uow.commit()

    def terminar_partida(self, id_partida: str, id_ganador: str):
        repo_partida: IPartidaJugadaRepository = self.uow.get_repository("partida")
        resultado = terminar_partida(id_partida, id_ganador, repo_partida)
        self.uow.commit()
        return resultado

    def listar_partidas_de_jugador(self, id_jugador: str):
        repo_partida: IPartidaJugadaRepository = self.uow.get_repository("partida")
        return listar_partidas_jugador(id_jugador, repo_partida)

    def obtener_jugadas_de_partida(self, id_partida: str):
        repo_jugada: IPartidaJugadaRepository = self.uow.get_repository("jugada")
        return obtener_jugadas_por_partida(id_partida, repo_jugada)
