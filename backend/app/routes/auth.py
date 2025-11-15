# backend/routes/auth.py
from fastapi import APIRouter, HTTPException, status
from backend.models.models import (
    LoginRequest, 
    LoginResponse, 
    Usuario, 
    SectorType, 
    NivelAcceso,
    PermisoType
)
from backend.services.recaptcha_service import recaptcha_service
from backend.app.middleware.auth_middleware import crear_token_sesion
from datetime import datetime
from typing import List

router = APIRouter(tags=["autenticacion"])

# Datos de prueba compatibles con tus modelos
usuarios_prueba = [
    Usuario(
        id=1,
        dui="12345678-9",
        nombres="Juan Carlos",
        apellidos="Pérez García",
        email="juan.perez@email.com",
        telefono="+503 1234-5678",
        sector=SectorType.CIUDADANO,
        nivel_acceso=NivelAcceso.CIUDADANO,
        created_at=datetime(2024, 1, 15, 10, 30, 0),
        is_active=True
    ),
    Usuario(
        id=2,
        dui="98765432-1",
        nombres="María Elena",
        apellidos="Rodríguez López", 
        email="maria.rodriguez@email.com",
        telefono="+503 8765-4321",
        sector=SectorType.MEDICO,
        nivel_acceso=NivelAcceso.MEDICO,
        created_at=datetime(2024, 1, 10, 14, 20, 0),
        is_active=True
    ),
    Usuario(
        id=4,
        dui="11111111-1",
        nombres="Ana Patricia",
        apellidos="Gómez Hernández",
        email="ana.gomez@email.com",
        telefono="+503 1111-1111",
        sector=SectorType.EDUCATIVO,
        nivel_acceso=NivelAcceso.EDUCATIVO,
        created_at=datetime(2024, 1, 12, 16, 45, 0),
        is_active=True
    ),
    Usuario(
        id=5,
        dui="99999999-9",
        nombres="Pedro Antonio",
        apellidos="López Ramírez",
        email="pedro.lopez@email.com", 
        telefono="+503 9999-9999",
        sector=SectorType.ADMIN,
        nivel_acceso=NivelAcceso.ADMIN,
        created_at=datetime(2024, 1, 5, 8, 0, 0),
        is_active=True
    )
]

@router.post("/login", response_model=LoginResponse)
async def login(credenciales: LoginRequest):
    """
    Login con verificación reCAPTCHA
    """
    # 1. Verificar reCAPTCHA primero
    is_valid_captcha = await recaptcha_service.verify_recaptcha(
        credenciales.captcha_token
    )
    
    if not is_valid_captcha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verificación de seguridad fallida"
        )
    
    # 2. Luego verificar credenciales normales
    usuario = next((u for u in usuarios_prueba if u.dui == credenciales.dui), None)
    
    # Contraseña de prueba para desarrollo
    if not usuario or credenciales.password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # 3. Generar token
    token = crear_token_sesion(usuario)
    
    # 4. Determinar permisos
    permisos = obtener_permisos_por_sector(usuario.sector)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        usuario=usuario,
        permisos=permisos
    )

def obtener_permisos_por_sector(sector: SectorType) -> List[PermisoType]:
    """
    Obtener permisos basados en el sector del usuario.
    """
    permisos_base = [PermisoType.LECTURA_PROPIA, PermisoType.ESCRITURA_PROPIA]
    
    permisos_por_sector = {
        SectorType.CIUDADANO: permisos_base,
        SectorType.MEDICO: permisos_base + [PermisoType.LECTURA_SALUD, PermisoType.ESCRITURA_SALUD],
        SectorType.EDUCATIVO: permisos_base + [PermisoType.LECTURA_EDUCACION, PermisoType.ESCRITURA_EDUCACION],
        SectorType.LABORAL: permisos_base + [PermisoType.LECTURA_LABORAL, PermisoType.ESCRITURA_LABORAL],
        SectorType.JUDICIAL: permisos_base + [PermisoType.LECTURA_JUDICIAL, PermisoType.ESCRITURA_JUDICIAL],
        SectorType.SERVICIOS_SOCIALES: permisos_base + [PermisoType.LECTURA_SERVICIOS_SOCIALES, PermisoType.ESCRITURA_SERVICIOS_SOCIALES],
        SectorType.ADMIN: [PermisoType.LECTURA_GLOBAL, PermisoType.ESCRITURA_GLOBAL] + permisos_base
    }
    
    return permisos_por_sector.get(sector, permisos_base)

# Endpoint para obtener tokens de prueba
@router.get("/test-tokens")
async def get_test_tokens():
    """Obtener lista de tokens de prueba para desarrollo"""
    tokens = []
    for usuario in usuarios_prueba:
        tokens.append({
            "id": usuario.id,
            "dui": usuario.dui,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "sector": usuario.sector.value,
            "nivel_acceso": usuario.nivel_acceso.value,
            "token_prueba": f"test_token_{usuario.id}",
            "password": "password123"
        })
    return {"tokens": tokens}

# Endpoint de health check
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Authentication API"}