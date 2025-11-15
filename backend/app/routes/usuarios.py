from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from backend.models.models import Usuario, UsuarioCompleto, SectorType
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import usuarios_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[Usuario])
async def listar_usuarios(
    sector: Optional[SectorType] = Query(None, description="Filtrar por sector"),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar usuarios según permisos"""
    from backend.app.middleware.auth_middleware import usuarios_prueba
    
    # Combinar usuarios de prueba y base de datos
    todos_usuarios = usuarios_prueba + usuarios_db
    
    # Admin ve todos
    if AuthorizationService.get_nivel_acceso(current_user) >= 7:  # ADMIN
        usuarios_filtrados = todos_usuarios
    else:
        # Usuarios normales solo se ven a sí mismos
        usuarios_filtrados = [u for u in todos_usuarios if u.id == current_user.id]
    
    if sector:
        usuarios_filtrados = [u for u in usuarios_filtrados if u.sector == sector]
    
    return usuarios_filtrados

@router.get("/{usuario_id}", response_model=UsuarioCompleto)
async def obtener_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener usuario específico con control de acceso"""
    from backend.app.routes.auth import get_usuario_completo
    
    # Verificar permisos
    if not AuthorizationService.puede_ver_usuario(current_user, usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    usuario_completo = get_usuario_completo(usuario_id)
    if not usuario_completo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Filtrar datos según permisos
    datos_filtrados = AuthorizationService.filtrar_datos_usuario(
        current_user, 
        usuario_completo.dict()
    )
    
    return UsuarioCompleto(**datos_filtrados)

@router.put("/{usuario_id}/info-basica")
async def actualizar_info_basica(
    usuario_id: int,
    info_actualizada: dict,
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar información básica del usuario"""
    from backend.app.middleware.auth_middleware import usuarios_prueba
    
    # Solo puede editar su propia información básica
    if usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes editar tu propia información"
        )
    
    # Buscar en usuarios de prueba
    usuario = next((u for u in usuarios_prueba if u.id == usuario_id), None)
    
    # Si no está en prueba, buscar en base de datos normal
    if not usuario:
        usuario = next((u for u in usuarios_db if u.id == usuario_id), None)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos permitidos
    campos_permitidos = ['email', 'telefono', 'direccion']
    for campo in campos_permitidos:
        if campo in info_actualizada:
            setattr(usuario, campo, info_actualizada[campo])
    
    return {"message": "Información actualizada exitosamente", "usuario": usuario}