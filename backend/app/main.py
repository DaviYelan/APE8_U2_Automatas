"""
main.py
=======
Punto de entrada de la aplicación FastAPI.

Configuración:
  - CORS habilitado para desarrollo local (React en puerto 5173)
  - Router principal montado en la raíz
  - Documentación automática en /docs (Swagger UI)

Ejecución:
  uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

# ------------------------------------------------------------------ #
#  Crear instancia de FastAPI
# ------------------------------------------------------------------ #
app = FastAPI(
    title="CFG Boolean Expression Analyzer",
    description=(
        "API para el análisis de expresiones lógicas booleanas "
        "mediante una Gramática Libre de Contexto (CFG). "
        "Realiza tokenización, validación sintáctica, "
        "generación de derivaciones y construcción de árboles sintácticos."
    ),
    version="1.0.0",
)

# ------------------------------------------------------------------ #
#  Middleware CORS (permitir peticiones del frontend React)
# ------------------------------------------------------------------ #
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # React dev alternativo
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------ #
#  Registrar rutas
# ------------------------------------------------------------------ #
app.include_router(router)
