import datetime
from dataclasses import dataclass


@dataclass
class Jugador:
    id: str
    nombre: str
    correo: str
