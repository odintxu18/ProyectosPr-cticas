from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="X-API-Key")


API_KEYS = {
    "5f0c7127-3be9-4488-b801-c7b6415b45e9": {
        "username": "jugador_demo",
        "role": "player",
    },
}


def check_api_key(api_key: str):

    return api_key in API_KEYS


def get_user_from_api_key(api_key: str):

    return API_KEYS.get(api_key)


def get_user(api_key_header: str = Security(api_key_header)):

    if not api_key_header or not check_api_key(api_key_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )
    return get_user_from_api_key(api_key_header)
