from sqlmodel import SQLModel,create_engine, Session,select, func
from typing import  Annotated
from fastapi import Depends
from src.core.log import Logger
from src.model.modelo_core import Usuario, Sesion_juego
import os
from dotenv import load_dotenv
load_dotenv()
logger = Logger(log_file="app.log").get_logger()


connect_args = {"check_same_thread": False}
engine = create_engine(os.getenv("BD"),echo=True)
async def insertar_documento():
    SQLModel.metadata.create_all(engine)

def crear_sesion():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(crear_sesion)]

def guardar_BD(dato: SQLModel, session: Session):
    try:
        
        session.add(dato)
        session.commit()
        session.refresh(dato)
        return dato
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        

async def autenticar_usuario(usuario: str,  session: SessionDep):
    """
    Function to authenticate a user.
    """
    try:
        user = session.query(Usuario).filter(Usuario.nombre_usuario == usuario).first()
        if not user:
            return None
        return user
    except Exception as e:
        logger.error(f"Error during authentication: {str(e)}")
        raise e
        
async def obtener_usuario(session: SessionDep):
    """
    Function to get a user by username.
    """
    try:
        #consultar todos los usuario de Usuario
        usuario = session.query(Usuario).all()
        if not usuario:
            return None
        return usuario
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise e
        
async def detener_juego(session: SessionDep, usuario_id: int):
    """
    funcion para detener una sesion de juego
    """
    try:
        sesion = session.query(Sesion_juego).filter(Sesion_juego.usuario_id == usuario_id).order_by(Sesion_juego.id.desc()).first()
        if not sesion:
            return None
        return sesion
    except Exception as e:
        logger.error(f"Error retrieving game session: {str(e)}")
        raise e
        
        
async def tabla_clasificacion(session: SessionDep, limit: int = 10, offset: int = 0):
    """
    Function to get the leaderboard of game sessions.
    """
    try:
        statement = (select(Usuario.nombre_usuario,
                          func.count(Sesion_juego.id).label("total_juego"),
                          func.avg(Sesion_juego.desviacion).label("desviacion_avg"),
                          func.min(Sesion_juego.desviacion).label("mejor_desviacion"),                         
                          
                   )
                   
                    .join(Usuario, Usuario.id == Sesion_juego.usuario_id)
                    .group_by(Sesion_juego.usuario_id)
                    .order_by(func.avg(Sesion_juego.desviacion).asc())
                    .limit(limit)
                    .offset(offset)
        )
        results = session.exec(statement).all()
        if not results:
            return None
        return results
    except Exception as e:
        logger.error(f"Error retrieving leaderboard: {str(e)}")
        raise e
    
    
