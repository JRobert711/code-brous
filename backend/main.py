from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Importar todos los routers
from backend.app.routes.auth import router as auth_router
from backend.app.routes.usuarios import router as usuarios_router
from backend.app.routes.salud import router as salud_router
from backend.app.routes.educacion import router as educacion_router
from backend.app.routes.laboral import router as laboral_router
from backend.app.routes.judicial import router as judicial_router
from backend.app.routes.servicios_sociales import router as servicios_sociales_router

app = FastAPI(title="Sistema Nacional de Identidad", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(usuarios_router, prefix="/api")
app.include_router(salud_router, prefix="/api")
app.include_router(educacion_router, prefix="/api")
app.include_router(laboral_router, prefix="/api")
app.include_router(judicial_router, prefix="/api")
app.include_router(servicios_sociales_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "🏛️ Sistema Nacional de Identidad - Backend",
        "version": "1.0.0",
        "timestamp": datetime.now(),
        "modulos_activos": [
            "Autenticación",
            "Gestión de Usuarios", 
            "Salud",
            "Educación",
            "Laboral", 
            "Judicial",
            "Servicios Sociales"
        ],
        "endpoints": {
            "auth": "/api/auth",
            "usuarios": "/api/usuarios",
            "salud": "/api/salud",
            "educacion": "/api/educacion",
            "laboral": "/api/laboral",
            "judicial": "/api/judicial",
            "servicios_sociales": "/api/servicios-sociales",
            "docs": "/docs"
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "system": "Sistema Nacional de Identidad"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)