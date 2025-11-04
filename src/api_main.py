from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.jugador.handler.handler_jugador import app_jugador
from src.partida.handler.handler_jugada_partida import app_partida

main_app = FastAPI()

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)
main_app.include_router(app_partida, prefix="/tictactoe")
main_app.include_router(app_jugador, prefix="/tictactoe")


@main_app.get("/")
async def root():
    return {"message": "Hello from the tictctoe root!"}
