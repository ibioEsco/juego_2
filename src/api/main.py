from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from src.model.modelo_BD import insertar_documento
from src.api.login_api import router as enuratador_login
from src.api.usuario_api import router as enuratador_usuario
from src.api.juego_api import router as enuratador_juego


app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

app.include_router(enuratador_login, prefix="/v1", tags=["login"])
app.include_router(enuratador_usuario, prefix="/v1", tags=["usuario"])
app.include_router(enuratador_juego, prefix="/v1", tags=["juego"])





@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def app_init():
    await insertar_documento()
