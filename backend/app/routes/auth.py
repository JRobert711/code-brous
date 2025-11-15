# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

# Importaciones corregidas
from backend.models.models import (
    LoginRequest, 
    DocumentLoginRequest, 
    TokenResponse, 
    MessageResponse,
    Usuario,
    SectorType,
    NivelAcceso,
    PermisoType
)
from backend.database.connection.database import db_manager
from backend.app.middleware.auth_middleware import (
    crear_token_sesion, 
    eliminar_token_sesion, 
    get_current_user,
    obtener_usuario_por_id,
    usuarios_prueba as usuarios_prueba_middleware
)
from backend.services.recaptcha_service import recaptcha_service
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(tags=["autenticacion"])
security = HTTPBearer()

# Usar los usuarios del middleware para consistencia
usuarios_prueba = usuarios_prueba_middleware

# =============================
#  MODELOS TEMPORALES PARA EL FRONTEND
# =============================
class LoginRequestFrontend(BaseModel):
    dui: str
    password: str
    captcha_token: str  # ← frontend envía "captcha_token"

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario
    permisos: Dict[str, bool] = {}

# =============================
#  LOGIN PRINCIPAL (PARA TU FRONTEND ACTUAL)
# =============================
@router.post("/login", response_model=LoginResponse)
async def login(credenciales: LoginRequestFrontend):
    """
    Login principal que coincide con tu frontend React.
    Recibe 'captcha_token' en lugar de 'recaptcha_token'
    """
    # 1. Verificar reCAPTCHA primero
    is_valid_captcha = await recaptcha_service.verify_recaptcha(
        credenciales.captcha_token  # ← Usar captcha_token del frontend
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
    
    # 3. Generar token usando tu middleware
    token = crear_token_sesion(usuario)
    
    # 4. Determinar permisos basados en sector (formato que espera tu frontend)
    permisos_lista = obtener_permisos_por_sector(usuario.sector)
    permisos_dict = {permiso.value: True for permiso in permisos_lista}
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        usuario=usuario,
        permisos=permisos_dict
    )

# =============================
#  LOGIN CON DUI + reCAPTCHA (ALTERNATIVO)
# =============================
@router.post("/login-dui", response_model=TokenResponse)
async def login_dui(credenciales: LoginRequest):
    """
    Login usando DUI con verificación reCAPTCHA.
    """
    # 1. Verificar reCAPTCHA primero
    is_valid_captcha = await recaptcha_service.verify_recaptcha(
        credenciales.recaptcha_token
    )
    
    if not is_valid_captcha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verificación de seguridad fallida"
        )
    
    # 2. Luego verificar credenciales normales
    usuario = next((u for u in usuarios_prueba if u.dui == credenciales.dui), None)
    
    if not usuario or credenciales.password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # 3. Generar token
    token = crear_token_sesion(usuario)
    
    # 4. Determinar permisos basados en sector
    permisos = obtener_permisos_por_sector(usuario.sector)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=usuario,
        permisos=permisos
    )

# =============================
#  LOGIN CON DOCUMENTO + reCAPTCHA
# =============================
@router.post("/login-documento", response_model=TokenResponse)
async def login_documento(credenciales: DocumentLoginRequest):
    """
    Login usando tipo + número de identificación con reCAPTCHA.
    """
    # 1. Verificar reCAPTCHA
    is_valid_captcha = await recaptcha_service.verify_recaptcha(
        credenciales.recaptcha_token
    )
    
    if not is_valid_captcha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verificación de seguridad fallida"
        )

    tipo = credenciales.document_type
    numero = credenciales.document_value
    password = credenciales.password

    if not tipo or not numero:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="document_type y document_value son obligatorios"
        )

    # En producción verificarías la contraseña hasheada
    if password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    conn = db_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombres, apellidos, email, tipo_identificacion, numero_identificacion
        FROM usuarios
        WHERE tipo_identificacion=? AND numero_identificacion=?
    """, (tipo, numero))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    # Buscar si el usuario existe en nuestros datos de prueba
    usuario_existente = next((u for u in usuarios_prueba if str(u.id) == str(row[0])), None)
    
    if usuario_existente:
        # Usar usuario existente de los datos de prueba
        usuario_db = usuario_existente
    else:
        # Crear nuevo objeto Usuario desde la base de datos
        usuario_db = Usuario(
            id=row[0],
            dui=row[5],  # Usar numero_identificacion como DUI
            nombres=row[1],
            apellidos=row[2],
            email=row[3],
            sector=SectorType.CIUDADANO,
            nivel_acceso=NivelAcceso.CIUDADANO,
            created_at=datetime.now(),
            is_active=True
        )

    # Token real usando tu middleware
    token = crear_token_sesion(usuario_db)
    permisos = obtener_permisos_por_sector(usuario_db.sector)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=usuario_db,
        permisos=permisos
    )

# =============================
#  LOGIN RÁPIDO PARA DESARROLLO
# =============================
@router.post("/login-desarrollo/{usuario_id}", response_model=LoginResponse)
async def login_desarrollo(usuario_id: int):
    """
    Login rápido para desarrollo usando ID de usuario.
    """
    usuario = obtener_usuario_por_id(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Generar token de prueba (compatible con tu middleware)
    token = f"test_token_{usuario.id}"
    permisos_lista = obtener_permisos_por_sector(usuario.sector)
    permisos_dict = {permiso.value: True for permiso in permisos_lista}

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        usuario=usuario,
        permisos=permisos_dict
    )

# =============================
#  LISTAR USUARIOS DE PRUEBA
# =============================
@router.get("/usuarios-prueba")
async def listar_usuarios_prueba():
    """
    Listar todos los usuarios de prueba disponibles para desarrollo.
    """
    return {
        "usuarios": [
            {
                "id": usuario.id,
                "dui": usuario.dui,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos,
                "sector": usuario.sector.value,
                "nivel_acceso": usuario.nivel_acceso.value,
                "token_prueba": f"test_token_{usuario.id}"
            }
            for usuario in usuarios_prueba
        ]
    }

# =============================
#  OBTENER USUARIO ACTUAL
# =============================
@router.get("/me", response_model=Usuario)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user

# =============================
#  VERIFICAR PERMISOS
# =============================
@router.get("/verificar-permisos")
async def verificar_permisos(current_user: Usuario = Depends(get_current_user)):
    """
    Verificar permisos del usuario actual.
    """
    permisos = obtener_permisos_por_sector(current_user.sector)
    permisos_dict = {permiso.value: True for permiso in permisos}
    
    return {
        "usuario": current_user,
        "permisos": permisos_dict,
        "sector": current_user.sector.value,
        "nivel_acceso": current_user.nivel_acceso.value
    }

# =============================
#  LOGOUT
# =============================
@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: Usuario = Depends(get_current_user), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    eliminar_token_sesion(token)
    return MessageResponse(message="Sesión cerrada exitosamente")

# =============================
#  FUNCIONES AUXILIARES
# =============================
def obtener_permisos_por_sector(sector: SectorType) -> list:
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