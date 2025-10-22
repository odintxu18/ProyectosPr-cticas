from fastapi import FastAPI
from api import APIJuego

app = FastAPI()

# Crear instancia de la clase API y montar el router
api_juego = APIJuego()
app.include_router(api_juego.router)
