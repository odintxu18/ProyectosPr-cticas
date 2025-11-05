from src.partida.domain.jugada import Jugada
from src.partida.domain.partida import Partida


from src.shared.dbmodels.dbmodels import (
    Partida as PartidaModel,
    Jugada as JugadaModel,
)
from src.partida.repository.Jugada_partida_repository import IPartidaJugadaRepository
from src.shared.sql_alchemy_interface import SqlAlchemyInterface


class PartidaJugadaRepositorySQLAlchemy(IPartidaJugadaRepository, SqlAlchemyInterface):

    def agregar_partida(self, game: Partida) -> Partida:

        partida_model = PartidaModel(
            id=game.id,
            id_jugador_x=game.id_jugador_x,
            id_jugador_o=game.id_jugador_o,
            fecha_inicio=game.fecha_inicio,
            fecha_fin=game.fecha_fin,
            id_ganador=game.id_ganador,
        )
        self.session.add(partida_model)
        self.session.commit()

        return Partida(
            id=partida_model.id,
            id_jugador_x=partida_model.id_jugador_x,
            id_jugador_o=partida_model.id_jugador_o,
            fecha_inicio=partida_model.fecha_inicio,
            fecha_fin=partida_model.fecha_fin,
            id_ganador=partida_model.id_ganador,
        )

    def obtener_partida_por_id(self, partida_id: str) -> Partida | None:
        partida_model = self.session.get(PartidaModel, partida_id)
        if partida_model:
            return Partida(
                id=partida_model.id,
                id_jugador_x=partida_model.id_jugador_x,
                id_jugador_o=partida_model.id_jugador_o,
                fecha_inicio=partida_model.fecha_inicio,
                fecha_fin=partida_model.fecha_fin,
                id_ganador=partida_model.id_ganador,
            )
        return None

    def listar_partidas(self) -> list[Partida]:
        partidas = self.session.query(PartidaModel).all()
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
        ]

    def actualizar_partida(self, game: Partida) -> bool:
        try:
            partida_model = self.session.get(PartidaModel, game.id)
            if not partida_model:
                return False

            partida_model.fecha_fin = game.fecha_fin
            partida_model.id_ganador = game.id_ganador

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_partida(self, id_partida: str) -> bool:
        try:
            eliminado = (
                self.session.query(PartidaModel).filter_by(id=id_partida).delete()
            )
            self.session.commit()
            return eliminado > 0
        except Exception as e:
            self.session.rollback()
            raise e

    def agregar_jugada(self, play: Jugada) -> Jugada:

        jugada_model = JugadaModel(
            id=play.id,
            id_partida=play.id_partida,
            id_jugador=play.id_jugador,
            turno=play.turno,
            fila=play.fila,
            columna=play.columna,
            fecha_jugada=play.fecha_jugada,
        )
        self.session.add(jugada_model)
        self.session.commit()
        return Jugada(
            id=jugada_model.id,
            id_partida=jugada_model.id_partida,
            id_jugador=jugada_model.id_jugador,
            turno=jugada_model.turno,
            fila=jugada_model.fila,
            columna=jugada_model.columna,
            fecha_jugada=jugada_model.fecha_jugada,
        )

    def obtener_jugada_por_id(self, id_jugada: str) -> Jugada | None:
        jugada_model = self.session.get(JugadaModel, id_jugada)
        if jugada_model:
            return Jugada(
                id=jugada_model.id,
                id_partida=jugada_model.id_partida,
                id_jugador=jugada_model.id_jugador,
                turno=jugada_model.turno,
                fila=jugada_model.fila,
                columna=jugada_model.columna,
                fecha_jugada=jugada_model.fecha_jugada,
            )
        print("id_jugada recibido:", id_jugada)
        print("jugada obtenida:", Jugada)

        return None

    def obtener_jugadas_por_partida(self, id_partida: str) -> list[Jugada]:

        jugadas_model = (
            self.session.query(JugadaModel)
            .filter_by(id_partida=id_partida)
            .order_by(JugadaModel.turno)
            .all()
        )
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
            for j in jugadas_model
        ]

    def eliminar_jugada(self, id_jugada: str) -> bool:
        try:
            eliminado = self.session.query(JugadaModel).filter_by(id=id_jugada).delete()
            self.session.commit()
            return eliminado > 0
        except Exception as e:
            self.session.rollback()
            raise e
