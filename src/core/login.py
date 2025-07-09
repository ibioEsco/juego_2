
from typing import Annotated
from src.core.log import Logger
from fastapi import HTTPException,Depends, status
from src.model.modelo_BD import SessionDep
from src.model.modelo_BD import autenticar_usuario
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
import time
import jwt
from jwt import InvalidTokenError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_SECONDS = int(os.getenv("TOKEN_EXPIRATION_SECONDS", 1800))
logger = Logger(log_file="app.log").get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.getenv("URL_BACK")+"/v1/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": time.time() + TOKEN_EXPIRATION_SECONDS})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


    
async def consulta_usuario_validar_token(token: Annotated[str, Depends(oauth2_scheme)], 
                                   session: SessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        usuario = await autenticar_usuario(session= session, usuario=username)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario incorrecto",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except InvalidTokenError:   
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expirado o invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )


    return usuario
    

