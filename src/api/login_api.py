
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, HTTPException, status,APIRouter
from pydantic import BaseModel
from src.model.modelo_BD import autenticar_usuario, SessionDep
from src.core.login import (create_access_token,
                            verify_password)




router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str
    
    



@router.post("/login")
async def login_for_access_token(session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    usuario = await autenticar_usuario( usuario=form_data.username, 
                              session=session)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = verify_password(form_data.password, usuario.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": form_data.username,
    }

    access_token = create_access_token(
        data=data
    )
    return Token(access_token=access_token,
                 token_type="bearer")
    
    

    



