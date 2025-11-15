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
    ),
    # Agregar usuarios faltantes
    Usuario(
        id=6,
        dui="66666666-6",
        nombres="Roberto José",
        apellidos="Hernández Castro",
        email="roberto.hernandez@email.com",
        telefono="+503 6666-6666",
        sector=SectorType.LABORAL,
        nivel_acceso=NivelAcceso.LABORAL,
        created_at=datetime(2024, 1, 3, 11, 0, 0)
    ),
    Usuario(
        id=7,
        dui="77777777-7",
        nombres="Laura Beatriz",
        apellidos="Silva Mendoza",
        email="laura.silva@email.com",
        telefono="+503 7777-7777",
        sector=SectorType.SERVICIOS_SOCIALES,
        nivel_acceso=NivelAcceso.SERVICIOS_SOCIALES,
        created_at=datetime(2024, 1, 7, 13, 30, 0)
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

# Inicializar algunos tokens de prueba para desarrollo
def inicializar_tokens_prueba():
    """Inicializar tokens de prueba para desarrollo"""
    print("🔄 Inicializando tokens de prueba...")
    for usuario in usuarios_prueba:
        token_prueba = f"test_token_{usuario.id}"
        usuarios_autenticados[token_prueba] = usuario
        print(f"   ✅ Token creado: {token_prueba} para {usuario.nombres} ({usuario.sector})")
    
    print("🎯 Tokens disponibles:")
    for token, usuario in usuarios_autenticados.items():
        if token.startswith("test_token_"):
            print(f"   🔑 {token}: {usuario.nombres} {usuario.apellidos} - {usuario.sector} (Nivel {usuario.nivel_acceso})")

# Ejecutar inicialización al importar el módulo
inicializar_tokens_prueba()