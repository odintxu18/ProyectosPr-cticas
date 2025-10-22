from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from juego import Juego

class Jugada(BaseModel):
    fila: int
    col: int

class APIJuego:
    def __init__(self):
        self.router = APIRouter()
        self.juego = Juego()
        self.definir_rutas()

    def definir_rutas(self):
        @self.router.post("/reiniciar")
        def reiniciar():
            self.juego = Juego()
            return {"mensaje": "Juego reiniciado"}

        @self.router.get("/tablero")
        def tablero():
            return {"tablero": self.juego.tablero.tablero}

        @self.router.get("/turno")
        def turno():
            if self.juego.ha_terminado():
                return {"mensaje": "El juego ha terminado."}
            return {"jugador": self.juego.obtener_jugador_actual()}

        @self.router.post("/jugar")
        def jugar(jugada: Jugada):
            if self.juego.ha_terminado():
                raise HTTPException(status_code=400, detail="El juego ya terminó.")

            if not (0 <= jugada.fila <= 2 and 0 <= jugada.col <= 2):
                raise HTTPException(status_code=400, detail="Posición fuera de rango.")

            if not self.juego.tablero.colocar(jugada.fila, jugada.col, self.juego.obtener_jugador_actual()):
                raise HTTPException(status_code=400, detail="Casilla ocupada.")

            if self.juego.tablero.comprobar_ganador(self.juego.obtener_jugador_actual()):
                self.juego.ganador = self.juego.obtener_jugador_actual()
                self.juego.terminado = True
                return {
                    "mensaje": f"¡El jugador {self.juego.ganador} ha ganado!",
                    "tablero": self.juego.tablero.tablero
                }

            if self.juego.tablero.esta_lleno():
                self.juego.terminado = True
                return {
                    "mensaje": "¡Empate!",
                    "tablero": self.juego.tablero.tablero
                }

            self.juego.cambiar_jugador()
            return {
                "mensaje": "Turno realizado.",
                "siguiente_turno": self.juego.obtener_jugador_actual(),
                "tablero": self.juego.tablero.tablero
            }

        @self.router.get("/estado")
        def estado():
            return {
                "tablero": self.juego.tablero.tablero,
                "jugador_actual": self.juego.obtener_jugador_actual(),
                "ganador": self.juego.obtener_ganador(),
                "terminado": self.juego.ha_terminado()
            }
