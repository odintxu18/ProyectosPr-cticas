import os
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

API_KEY = "mysecureapikey"
API_KEY_NAME = "X-API-KEY"


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def get_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return api_key
