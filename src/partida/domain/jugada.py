from dataclasses import dataclass
import datetime


@dataclass
class Jugada:
    id: str
    id_partida: str
    id_jugador: str
    turno: int
    fila: int
    columna: int
    fecha_jugada: datetime
