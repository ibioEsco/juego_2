from fastapi import (Depends, 
                     HTTPException,
                     APIRouter,
                     Query)
from src.model.modelo_BD import (SessionDep, 
                                 guardar_BD, 
                                 detener_juego,
                                 tabla_clasificacion)
from src.model.modelo_core import (Sesion_juego, 
                                   sesion_juego_core,
                                   Estadisticas_usuario)
from src.core.log import Logger
from src.core.login import consulta_usuario_validar_token
from typing import Annotated
from datetime import datetime


router = APIRouter()

logger = Logger(log_file="app.log").get_logger()

@router.post("/games/start", response_model= sesion_juego_core)
async def start_game(nueva_sesion: sesion_juego_core ,
                     session: SessionDep,
                     token: Annotated[str, Depends(consulta_usuario_validar_token)]):
    """
    Endpoint to start a new game session.
    """
    try:
        tiempo_inicio = nueva_sesion.hora_inicio 
        usuario_id = token.id
        registro_sesion  = Sesion_juego(
            usuario_id=usuario_id,
            hora_inicio=tiempo_inicio,
            hora_fin=None,
            duracion=None,  
            desviacion=None,
            estado=True  
        )
        
        

        registro = guardar_BD(dato=registro_sesion, session=session)
        
        if not registro:
            raise HTTPException(status_code=400, detail="Error starting game session")
        
        return {"message": "Game session started successfully"}
    
    except Exception as e:
        logger.error(f"Error starting game session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting game session: {str(e)}")



@router.post("/games/stop", response_model=Sesion_juego)
async def stop_game(
                    session: SessionDep,
                    terminar_juego: Annotated[str,Depends(detener_juego)],
                    token: Annotated[str, Depends(consulta_usuario_validar_token)],
                    ):
    """
    Endpoint to stop a game session.
    """
    try:
        sesion = terminar_juego
        
        sesion.hora_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        sesion.estado = False
        sesion.duracion = (datetime.strptime(sesion.hora_fin,"%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(sesion.hora_inicio, "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
        sesion.desviacion = abs(sesion.duracion - sesion.usuario.marca_tiempo)
        session.commit()
        session.refresh(sesion)
        
        return sesion
    
    except Exception as e:
        logger.error(f"Error stopping game session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error stopping game session: {str(e)}")
    
    
@router.get("/leaderboard", response_model=dict)
async def get_leaderboard(
    session: SessionDep,
    _: Annotated[str, Depends(consulta_usuario_validar_token)],
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    ):
    """
    Endpoint to get the leaderboard of game sessions.
    """
    try:
        sesiones = await tabla_clasificacion(
            session=session, 
            limit=limit, 
            offset=offset
        )
        registro = {"personas": []}
        for nombre_usuario, total_juegos, desviacion_avg, mejor_desviacion in sesiones:
            registro_tablero = {
                "nombre": nombre_usuario,
                "total_juego": total_juegos,
                "desviacion_avg": round(desviacion_avg, 2) if desviacion_avg is not None else None,
                "mejor_desviacion": mejor_desviacion
            }
            registro["personas"].append(registro_tablero)
        
        if not sesiones:
            raise HTTPException(status_code=404, detail="No game sessions found")
        
        return registro
    
    except Exception as e:
        logger.error(f"Error retrieving leaderboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving leaderboard: {str(e)}")
    
    
@router.get("/analytics/user/{user_id}", response_model=Estadisticas_usuario)
async def get_user_analytics(
    user_id: int,
    session: SessionDep,
    _: Annotated[str, Depends(consulta_usuario_validar_token)]
):
    """
    Endpoint to get user analytics.
    """
    try:
        sesiones = session.query(Sesion_juego).filter(Sesion_juego.usuario_id == user_id).all()
        if not sesiones:
            raise HTTPException(status_code=404, detail="No game sessions found for this user")
        
        tablero = []
        for sesion in sesiones:
            tablero.append({
                "nombre": sesion.usuario.nombre_usuario,
                "total_juego": len(sesiones),
                "desviacion_avg": round(sum(s.duracion for s in sesiones) / len(sesiones), 2),
                "mejor_desviacion": min(s.desviacion for s in sesiones)
            })
        
        return Estadisticas_usuario(tablero=tablero, sesiones=sesiones)
    
    except Exception as e:
        logger.error(f"Error retrieving user analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user analytics: {str(e)}")
    
