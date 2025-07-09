from fastapi import  HTTPException,APIRouter,Depends
from src.model.modelo_core import Usuario 
from src.model.modelo_BD import guardar_BD, SessionDep, obtener_usuario
from src.core.log import Logger
from src.core.login import hash_password, consulta_usuario_validar_token
from typing import Annotated


logger = Logger(log_file="app.log").get_logger()

router = APIRouter()

@router.post("/auth/register")
async def register_user(usuario: Usuario, session : SessionDep):
    """
    Endpoint to register a new user.
    """
    try:
        # Hash the password before saving it
        usuario.password = hash_password(usuario.password)
        registro = guardar_BD(dato=usuario,
                              session=session)
        if not registro:
            raise HTTPException(status_code=400, detail="User already exists")
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during registration: {str(e)}")
    
    
@router.get("/auth/user/")
async def get_user( session: SessionDep, token: Annotated[str, Depends(consulta_usuario_validar_token)]):
    """
    Endpoint to retrieve user information by username.
    """
    try:
        usuario = await obtener_usuario(session=session)

        if not usuario:
            raise HTTPException(status_code=404, detail="User not found")
        return {"usuario": usuario}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

