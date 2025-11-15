from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime
from backend.models.models import Usuario, SectorType, NivelAcceso

# Configuración de seguridad
security = HTTPBearer()

# Base de datos simulada de tokens
usuarios_autenticados = {}

# Datos de usuarios de prueba para desarrollo
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
        created_at=datetime(2024, 1, 15, 10, 30, 0)
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
        created_at=datetime(2024, 1, 10, 14, 20, 0)
    ),
    Usuario(
        id=3,
        dui="55555555-5",
        nombres="Carlos Alberto",
        apellidos="Martínez Sánchez", 
        email="carlos.martinez@email.com",
        telefono="+503 5555-5555",
        sector=SectorType.JUDICIAL,
        nivel_acceso=NivelAcceso.JUDICIAL,
        created_at=datetime(2024, 1, 8, 9, 15, 0)
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
        created_at=datetime(2024, 1, 12, 16, 45, 0)
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
        created_at=datetime(2024, 1, 5, 8, 0, 0)
    )
]

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Usuario:
    """
    Obtener el usuario actual basado en el token de autenticación.
    """
    token = credentials.credentials
    
    # En desarrollo, permitimos tokens de prueba
    if token.startswith("test_token_"):
        usuario_id = int(token.replace("test_token_", ""))
        usuario = next((u for u in usuarios_prueba if u.id == usuario_id), None)
        if usuario:
            return usuario
    
    # Verificar token en la base de datos de tokens activos
    usuario = usuarios_autenticados.get(token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado. Por favor, inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return usuario

async def get_optional_user(request: Request) -> Optional[Usuario]:
    """
    Obtener usuario actual, pero retorna None si no está autenticado.
    Esta versión usa el request directamente para evitar problemas de tipos.
    """
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None
    
    try:
        # Extraer el token del header Authorization
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        # Usar la lógica de get_current_user
        if token.startswith("test_token_"):
            usuario_id = int(token.replace("test_token_", ""))
            usuario = next((u for u in usuarios_prueba if u.id == usuario_id), None)
            if usuario:
                return usuario
        
        usuario = usuarios_autenticados.get(token)
        if usuario:
            return usuario
            
        return None
        
    except Exception:
        return None

def crear_token_sesion(usuario: Usuario) -> str:
    """
    Crear un nuevo token de sesión para un usuario.
    """
    import secrets
    
    # Generar token seguro
    token = f"live_token_{usuario.id}_{secrets.token_hex(16)}"
    
    # Guardar en la base de datos de tokens
    usuarios_autenticados[token] = usuario
    
    return token

def eliminar_token_sesion(token: str) -> bool:
    """
    Eliminar un token de sesión (logout).
    """
    if token in usuarios_autenticados:
        del usuarios_autenticados[token]
        return True
    return False

def obtener_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    """
    Obtener usuario por ID (para uso interno).
    """
    # Buscar en usuarios de prueba
    usuario = next((u for u in usuarios_prueba if u.id == usuario_id), None)
    if usuario:
        return usuario
    
    return None

def crear_usuario_admin_por_defecto():
    """Crear usuario admin por defecto si no existe"""
    admin_existente = next((u for u in usuarios_prueba if u.sector == SectorType.ADMIN), None)
    
    if not admin_existente:
        usuario_admin = Usuario(
            id=999,
            dui="00000000-0",
            nombres="Administrador",
            apellidos="del Sistema",
            email="admin@sistema.com",
            telefono="+503 0000-0000",
            sector=SectorType.ADMIN,
            nivel_acceso=NivelAcceso.ADMIN,
            created_at=datetime.now()
        )
        usuarios_prueba.append(usuario_admin)
        
        # Crear token para el admin
        token_admin = "test_token_999"
        usuarios_autenticados[token_admin] = usuario_admin
        print("✅ Usuario admin creado por defecto - Token: test_token_999")

# Inicializar algunos tokens de prueba para desarrollo
def inicializar_tokens_prueba():
    """Inicializar tokens de prueba para desarrollo"""
    for usuario in usuarios_prueba:
        token_prueba = f"test_token_{usuario.id}"
        usuarios_autenticados[token_prueba] = usuario

# Ejecutar inicialización al importar el módulo
inicializar_tokens_prueba()
crear_usuario_admin_por_defecto()