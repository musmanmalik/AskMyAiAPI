import os
from dotenv import load_dotenv
from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer

# Take environment variables from .env
load_dotenv()
jwt_key = os.environ.get("JWT_SECRET_KEY")
security = HTTPBearer()


async def validate_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
        Function that is used to validate the token
    """
    token = credentials.credentials

    try:
        jwt.decode(token, key=jwt_key)

    except JOSEError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e))