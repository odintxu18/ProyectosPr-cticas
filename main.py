from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from juego import Juego, MovimientoInvalido

class Jugada(BaseModel):
    fila: int
    col: int

class APIJuego:
    def __init__(self):
        self.router = APIRouter()
        self.juego = Juego()
        self.definir_rutas()

    def definir_rutas(self):
        @self.router.post("/jugar")
        def jugar(jugada: Jugada):
            if self.juego.ha_terminado():
                self.juego.reiniciar()

            try:
                self.juego.realizar_turno(jugada.fila, jugada.col)
            except MovimientoInvalido as e:
                raise HTTPException(status_code=400, detail=str(e))
            if  self.juego.hay_ganador():
                return "hay un ganador"


        @self.router.get("/estado")
        def estado():
            return {
                "tablero": self.juego.tablero.tablero,
                "jugador_actual": self.juego.obtener_jugador_actual(),
                "ganador": self.juego.obtener_ganador(),
                "terminado": self.juego.ha_terminado()
            }

app = FastAPI()


api_juego = APIJuego()
app.include_router(api_juego.router)
