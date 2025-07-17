import pytest
from httpx import AsyncClient
from fastapi import status
from src.api.main  import app
# Mock para el token de usuario
class FakeToken:
    def __init__(self, id):
        self.id = id

@pytest.fixture
def fake_token(monkeypatch):
    # Sobrescribe la dependencia para validar el token
    from src.core.login import consulta_usuario_validar_token
    async def fake_dep():
        return FakeToken(id=123)
    monkeypatch.setattr(consulta_usuario_validar_token, fake_dep)
    return fake_dep

@pytest.mark.asyncio
async def test_start_game_success(fake_token):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        nueva_sesion = {
            "hora_inicio": "2025-07-09T21:00:00"
        }
        response = await ac.post(
            "/games/start",
            json=nueva_sesion,
            headers={"Authorization": "Bearer fake"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Game session started successfully"

@pytest.mark.asyncio
async def test_start_game_fail(fake_token, monkeypatch):
    # Simula que guardar_BD retorna None
    from src.model.modelo_BD import guardar_BD
    monkeypatch.setattr(guardar_BD, lambda dato, session: None)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        nueva_sesion = {
            "hora_inicio": "2025-07-09T21:00:00"
        }
        response = await ac.post(
            "/games/start",
            json=nueva_sesion,
            headers={"Authorization": "Bearer fake"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Error starting game session"