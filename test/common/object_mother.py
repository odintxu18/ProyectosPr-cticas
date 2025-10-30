import uuid
from datetime import datetime

from src.shared.dbmodels.dbmodels import *


@staticmethod
def jugador_mother():
    return Jugador(
        id=str(uuid.uuid4()),
        nombre=f"Jugador_{uuid.uuid4().hex[:6]}",
        correo=f"Correo_{uuid.uuid4().hex[:6]}@testing.com",
    )


@staticmethod
def partida_mother(jugador_x: Jugador, jugador_o: Jugador):
    return Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=jugador_x.id,
        id_jugador_o=jugador_o.id,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        id_ganador=uuid.uuid4().hex,
    )


@staticmethod
def jugada_mother(partida: Partida, jugador: Jugador, turno=1, fila=0, columna=0):
    return Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=jugador.id,
        turno=turno,
        fila=fila,
        columna=columna,
        fecha_jugada=datetime.now(),
    )


@staticmethod
def nombre_mother():
    return f"Jugador_{uuid.uuid4().hex[:6]}"


@staticmethod
def correo_mother():
    return f"Correo_{uuid.uuid4().hex[:6]}@testing.com"
