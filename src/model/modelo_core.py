from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime



class Usuario(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_usuario: str = Field(max_length=50, index=True, unique=True)
    marca_tiempo: int = Field(max_length=50, default=None)
    email: EmailStr = Field(max_length=100, unique=True, index=True)
    password: str = Field(max_length=255)
    sesiones : List["Sesion_juego"] = Relationship(back_populates="usuario")
    
class sesion_juego_core(BaseModel):
    hora_inicio: datetime = Field(default= datetime.now())
    
class Sesion_juego(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    hora_inicio: Optional[str] = Field(max_length=50, default=None)
    hora_fin: Optional[str] = Field(max_length=50, default=None)
    duracion: Optional[int]= Field(default=None)
    desviacion: Optional[int]= Field(default=None)
    estado: bool = Field( default=None)
    usuario: Usuario = Relationship(back_populates="sesiones")
    
class Tablero_juego(BaseModel):
    nombre: str
    total_juego: float
    desviacion_avg: float
    mejor_desviacion: float
    
class Estadisticas_usuario(BaseModel):
    tablero : List[Tablero_juego] 
    sesiones : List[Sesion_juego] 
    