from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.models import ExperienciaLaboral, HabilidadVerificada, ContribucionISSS, Usuario
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import experiencia_laboral_db, habilidades_verificadas_db, contribuciones_isss_db, get_next_id

router = APIRouter(prefix="/laboral", tags=["laboral"])

@router.get("/{usuario_id}/experiencia", response_model=List[ExperienciaLaboral])
async def obtener_experiencia(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener experiencia laboral de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'laboral'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al módulo laboral"
        )
    
    experiencia = [e for e in experiencia_laboral_db if e['usuario_id'] == usuario_id]
    return [ExperienciaLaboral(**e) for e in experiencia]

@router.post("/{usuario_id}/experiencia")
async def agregar_experiencia(
    usuario_id: int,
    experiencia: ExperienciaLaboral,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva experiencia laboral"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'laboral'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar experiencia laboral"
        )
    
    nueva_experiencia = experiencia.dict()
    nueva_experiencia['id'] = get_next_id()
    nueva_experiencia['usuario_id'] = usuario_id
    experiencia_laboral_db.append(nueva_experiencia)
    
    return {"message": "Experiencia laboral agregada exitosamente"}

@router.get("/{usuario_id}/habilidades", response_model=List[HabilidadVerificada])
async def obtener_habilidades(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener habilidades verificadas de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'laboral'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a habilidades")
    
    habilidades = [h for h in habilidades_verificadas_db if h['usuario_id'] == usuario_id]
    return [HabilidadVerificada(**h) for h in habilidades]

@router.post("/{usuario_id}/habilidades")
async def agregar_habilidad(
    usuario_id: int,
    habilidad: HabilidadVerificada,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva habilidad verificada"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'laboral'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar habilidades")
    
    nueva_habilidad = habilidad.dict()
    nueva_habilidad['id'] = get_next_id()
    nueva_habilidad['usuario_id'] = usuario_id
    habilidades_verificadas_db.append(nueva_habilidad)
    
    return {"message": "Habilidad verificada agregada exitosamente"}

@router.get("/{usuario_id}/isss", response_model=List[ContribucionISSS])
async def obtener_contribuciones_isss(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener contribuciones al ISSS de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'laboral'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a contribuciones ISSS")
    
    contribuciones = [c for c in contribuciones_isss_db if c['usuario_id'] == usuario_id]
    return [ContribucionISSS(**c) for c in contribuciones]

@router.post("/{usuario_id}/isss")
async def agregar_contribucion_isss(
    usuario_id: int,
    contribucion: ContribucionISSS,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva contribución al ISSS"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'laboral'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar contribuciones ISSS")
    
    nueva_contribucion = contribucion.dict()
    nueva_contribucion['id'] = get_next_id()
    nueva_contribucion['usuario_id'] = usuario_id
    contribuciones_isss_db.append(nueva_contribucion)
    
    return {"message": "Contribución al ISSS agregada exitosamente"}