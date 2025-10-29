import datetime
from dataclasses import dataclass


@dataclass
class Partida:
    id: int
    id_jugador_x: int
    id_jugador_o: int
    fecha_inicio: datetime
    fecha_final: datetime
    id_ganador: int
