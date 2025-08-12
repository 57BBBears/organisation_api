from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from src.config import config

api_key_header = APIKeyHeader(name="X-API-Key")


def check_auth(api_key: str = Security(api_key_header)) -> bool:
    # Not for production. Just for demonstration purpose
    if api_key == config.api_secret_key:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key."
    )
