from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

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
API_KEY = "mysecureapikey"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    """Dependency to verify API key"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
        )
    return api_key


main_app.include_router(app_partida, prefix="/tictactoe")
main_app.include_router(app_jugador, prefix="/tictactoe")


@main_app.get("/")
async def root():
    return {"message": "Hello from the tictctoe root!"}
