from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from backend.models.models import Usuario, UsuarioCreate, UsuarioCompleto, SectorType, NivelAcceso
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user, crear_token_sesion, eliminar_token_sesion
from backend.app.shared_data import usuarios_db, next_id

router = APIRouter(tags=["autenticacion"])
security = HTTPBearer()

@router.post("/register", response_model=Usuario)
async def register(usuario_data: UsuarioCreate):
    """Registrar nuevo usuario"""
    global next_id
    
    # Verificar si el DUI ya existe (en usuarios de prueba y base de datos)
    from backend.app.middleware.auth_middleware import usuarios_prueba
    if any(u.dui == usuario_data.dui for u in usuarios_prueba) or any(u.dui == usuario_data.dui for u in usuarios_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DUI ya está registrado"
        )
    
    # Crear un objeto Usuario temporal para calcular el nivel de acceso
    usuario_temp = Usuario(
        id=0,  # ID temporal
        dui=usuario_data.dui,
        nombres=usuario_data.nombres,
        apellidos=usuario_data.apellidos,
        email=usuario_data.email,
        telefono=usuario_data.telefono,
        fecha_nacimiento=usuario_data.fecha_nacimiento,
        direccion=usuario_data.direccion,
        sector=usuario_data.sector,
        nivel_acceso=NivelAcceso.CIUDADANO,  # Valor por defecto
        created_at=datetime.now()
    )
    
    nuevo_usuario = Usuario(
        id=next_id,
        dui=usuario_data.dui,
        nombres=usuario_data.nombres,
        apellidos=usuario_data.apellidos,
        email=usuario_data.email,
        telefono=usuario_data.telefono,
        fecha_nacimiento=usuario_data.fecha_nacimiento,
        direccion=usuario_data.direccion,
        sector=usuario_data.sector,
        nivel_acceso=AuthorizationService.get_nivel_acceso(usuario_temp),
        created_at=datetime.now()
    )
    
    usuarios_db.append(nuevo_usuario)
    next_id += 1
    
    return nuevo_usuario

@router.post("/login")
async def login(credenciales: dict):
    """Login de usuario"""
    dui = credenciales.get("dui")
    password = credenciales.get("password")
    
    # Buscar en usuarios de prueba primero
    from backend.app.middleware.auth_middleware import usuarios_prueba
    usuario = next((u for u in usuarios_prueba if u.dui == dui), None)
    
    # Si no está en prueba, buscar en base de datos normal
    if not usuario:
        usuario = next((u for u in usuarios_db if u.dui == dui), None)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # En un sistema real, verificarías la contraseña hasheada
    # Aquí es solo simulación - password por defecto para testing
    if password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Generar token real usando la función del middleware
    token = crear_token_sesion(usuario)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario,
        "permisos": AuthorizationService.get_permisos_usuario(usuario)
    }

@router.get("/me", response_model=Usuario)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.post("/logout")
async def logout(
    current_user: Usuario = Depends(get_current_user), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Cerrar sesión"""
    token = credentials.credentials
    eliminar_token_sesion(token)
    
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/test-tokens")
async def get_test_tokens():
    """Endpoint para obtener tokens de prueba (solo desarrollo)"""
    tokens_prueba = []
    from backend.app.middleware.auth_middleware import usuarios_prueba
    
    for usuario in usuarios_prueba:
        tokens_prueba.append({
            "usuario": f"{usuario.nombres} {usuario.apellidos}",
            "sector": usuario.sector,
            "nivel_acceso": usuario.nivel_acceso,
            "token": f"test_token_{usuario.id}",
            "permisos": AuthorizationService.get_permisos_usuario(usuario)
        })
    
    return {
        "message": "Tokens de prueba para desarrollo",
        "tokens": tokens_prueba
    }

# Función auxiliar para otros routers
def get_usuario_completo(usuario_id: int):
    """Obtener usuario completo con todos sus datos"""
    from backend.app.middleware.auth_middleware import usuarios_prueba
    from backend.models.models import UsuarioCompleto
    
    # Buscar en usuarios de prueba
    usuario = next((u for u in usuarios_prueba if u.id == usuario_id), None)
    
    # Si no está en prueba, buscar en base de datos normal
    if not usuario:
        usuario = next((u for u in usuarios_db if u.id == usuario_id), None)
    
    if not usuario:
        return None
    
    # En un sistema real, aquí cargarías los datos de los diferentes módulos
    # Por ahora retornamos un usuario básico
    return UsuarioCompleto(
        **usuario.dict(),
        permisos=AuthorizationService.get_permisos_usuario(usuario)
    )