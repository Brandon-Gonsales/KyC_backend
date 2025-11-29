from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Importamos el router que contiene los 5 endpoints de estudiantes
from .routes.estudiante_routes import router as estudiantes_router

# Cargamos las variables de entorno (como MONGO_URL) del archivo .env
load_dotenv()

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Estudiantes",
    description="Un CRUD completo para gestionar estudiantes, construido con FastAPI y MongoDB.",
    version="1.0.0",
    # Configuración para que la documentación interactiva funcione correctamente
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluimos el router de estudiantes en la aplicación principal.
# Todos los endpoints de ese router ahora estarán disponibles bajo el prefijo "/estudiantes"
# Por ejemplo, el endpoint POST "/" del router se convertirá en "POST /estudiantes/"
app.include_router(estudiantes_router, tags=["Estudiantes"], prefix="/estudiantes")

# Creamos un endpoint raíz para verificar que la API está funcionando
@app.get("/")
def read_root():
    """
    Endpoint raíz de bienvenida.
    """
    return {"mensaje": "Bienvenido a la API de Estudiantes. Visita /docs para ver la documentación interactiva."}