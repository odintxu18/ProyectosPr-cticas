import datetime
from dataclasses import dataclass


@dataclass
class Partida:
    id: str
    id_jugador_x: str
    id_jugador_o: str
    fecha_inicio: datetime
    fecha_final: datetime
    id_ganador: str
