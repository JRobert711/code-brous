from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.models import Pension, Subsidio, AyudaEstatal, Usuario
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import pensiones_db, subsidios_db, ayudas_estatales_db, get_next_id

router = APIRouter(prefix="/servicios-sociales", tags=["servicios-sociales"])

@router.get("/{usuario_id}/pensiones", response_model=List[Pension])
async def obtener_pensiones(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener pensiones de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al módulo de servicios sociales"
        )
    
    pensiones = [p for p in pensiones_db if p['usuario_id'] == usuario_id]
    return [Pension(**p) for p in pensiones]

@router.post("/{usuario_id}/pensiones")
async def agregar_pension(
    usuario_id: int,
    pension: Pension,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva pensión"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar pensiones"
        )
    
    nueva_pension = pension.dict()
    nueva_pension['id'] = get_next_id()
    nueva_pension['usuario_id'] = usuario_id
    pensiones_db.append(nueva_pension)
    
    return {"message": "Pensión agregada exitosamente"}

@router.get("/{usuario_id}/subsidios", response_model=List[Subsidio])
async def obtener_subsidios(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener subsidios de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a subsidios")
    
    subsidios = [s for s in subsidios_db if s['usuario_id'] == usuario_id]
    return [Subsidio(**s) for s in subsidios]

@router.post("/{usuario_id}/subsidios")
async def agregar_subsidio(
    usuario_id: int,
    subsidio: Subsidio,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nuevo subsidio"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar subsidios")
    
    nuevo_subsidio = subsidio.dict()
    nuevo_subsidio['id'] = get_next_id()
    nuevo_subsidio['usuario_id'] = usuario_id
    subsidios_db.append(nuevo_subsidio)
    
    return {"message": "Subsidio agregado exitosamente"}

@router.get("/{usuario_id}/ayudas", response_model=List[AyudaEstatal])
async def obtener_ayudas(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener ayudas estatales de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a ayudas estatales")
    
    ayudas = [a for a in ayudas_estatales_db if a['usuario_id'] == usuario_id]
    return [AyudaEstatal(**a) for a in ayudas]

@router.post("/{usuario_id}/ayudas")
async def agregar_ayuda(
    usuario_id: int,
    ayuda: AyudaEstatal,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva ayuda estatal"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'servicios_sociales'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar ayudas estatales")
    
    nueva_ayuda = ayuda.dict()
    nueva_ayuda['id'] = get_next_id()
    nueva_ayuda['usuario_id'] = usuario_id
    ayudas_estatales_db.append(nueva_ayuda)
    
    return {"message": "Ayuda estatal agregada exitosamente"}