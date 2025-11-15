from fastapi import FastAPI
from app.api.routes.hello import router as hello_router
from app.api.routes.auth import router as auth_router
from app.api.routes.ciudadanos import router as ciudadanos_router

# Módulos avanzados CON dependencias funcionando
from app.api.routes.voice_advanced import router as voice_advanced_router
from app.api.routes.biometria_avanzada import router as biometria_avanzada_router

app = FastAPI()

# Routers básicos
app.include_router(hello_router, prefix="/api", tags=["hello"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(ciudadanos_router, prefix="/api/ciudadanos", tags=["ciudadanos"])

# Routers avanzados CON dependencias funcionando
app.include_router(voice_advanced_router, prefix="/api/advanced", tags=["voice-advanced"])
app.include_router(biometria_avanzada_router, prefix="/api/biometria", tags=["biometria-avanzada"])

@app.get("/")
def root():
    return {
        "message": "🚀 IDN SV Backend AVANZADO funcionando",
        "version": "3.0",
        "modulos_activos": [
            "Autenticación básica",
            "Gestión de ciudadanos", 
            "SpeechRecognition - Procesamiento de voz",
            "OpenCV - Procesamiento de imágenes",
            "Sistema de biometría avanzado"
        ],
        "endpoints_avanzados": {
            "voice_processing": "/api/advanced",
            "image_analysis": "/api/biometria/analyze-image",
            "system_stats": "/api/biometria/system-stats",
            "docs": "/docs"
        }
    }