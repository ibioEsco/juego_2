# Xpert API

API REST para gestión de usuarios y para un juergo, desarrollada con **FastAPI**, **SQLite** y desplegada con **Docker**.

---

## Características

- Autenticación segura con JWT.
- Gestión de usuarios y login.
- Persistencia de datos en SQLite
- Contenedores orquestados con Docker.

---

## Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- (Opcional para desarrollo) Python 3.11+

---

## Instalación y ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/ibioEsco/juego/
cd juego
```

### 2. Configura el archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con tus variables de entorno, por ejemplo:

```
DB= sqlite:///./
SECRET_KEY=tu_clave_secreta
```

### 3. Construye y levanta los servicios con Docker

```bash
docker build -t mi-servidor-python .
docker run -p 8000:8000 mi-servidor-python
```

Esto levantará dos contenedores:
- **fastapi-app**: API FastAPI.

### 4. Accede a la documentación interactiva

Abre en tu navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Estructura del proyecto

```
Juego/
├── src/
│   ├── api/
│   ├── core/
│   └── model/
|   └── test/
|   └── util/
├── requirements.txt
├── Dockerfile
└── .env
```




## Notas

- El archivo `.env` **pedirlo al administrador*.


---

## Licencia

MIT
