from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.models import AntecedentePenal, LicenciaConducir, MultaSancion, Usuario
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import antecedentes_penales_db, licencias_conducir_db, multas_sanciones_db, get_next_id

router = APIRouter(prefix="/judicial", tags=["judicial"])

@router.get("/{usuario_id}/antecedentes", response_model=List[AntecedentePenal])
async def obtener_antecedentes(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener antecedentes penales de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'judicial'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al módulo judicial"
        )
    
    antecedentes = [a for a in antecedentes_penales_db if a['usuario_id'] == usuario_id]
    return [AntecedentePenal(**a) for a in antecedentes]

@router.post("/{usuario_id}/antecedentes")
async def agregar_antecedente(
    usuario_id: int,
    antecedente: AntecedentePenal,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nuevo antecedente penal"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'judicial'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar antecedentes penales"
        )
    
    nuevo_antecedente = antecedente.dict()
    nuevo_antecedente['id'] = get_next_id()
    nuevo_antecedente['usuario_id'] = usuario_id
    antecedentes_penales_db.append(nuevo_antecedente)
    
    return {"message": "Antecedente penal agregado exitosamente"}

@router.get("/{usuario_id}/licencias", response_model=List[LicenciaConducir])
async def obtener_licencias(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener licencias de conducir de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'judicial'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a licencias")
    
    licencias = [l for l in licencias_conducir_db if l['usuario_id'] == usuario_id]
    return [LicenciaConducir(**l) for l in licencias]

@router.post("/{usuario_id}/licencias")
async def agregar_licencia(
    usuario_id: int,
    licencia: LicenciaConducir,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva licencia de conducir"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'judicial'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar licencias")
    
    nueva_licencia = licencia.dict()
    nueva_licencia['id'] = get_next_id()
    nueva_licencia['usuario_id'] = usuario_id
    licencias_conducir_db.append(nueva_licencia)
    
    return {"message": "Licencia de conducir agregada exitosamente"}

@router.get("/{usuario_id}/multas", response_model=List[MultaSancion])
async def obtener_multas(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener multas y sanciones de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'judicial'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a multas")
    
    multas = [m for m in multas_sanciones_db if m['usuario_id'] == usuario_id]
    return [MultaSancion(**m) for m in multas]

@router.post("/{usuario_id}/multas")
async def agregar_multa(
    usuario_id: int,
    multa: MultaSancion,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva multa o sanción"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'judicial'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar multas")
    
    nueva_multa = multa.dict()
    nueva_multa['id'] = get_next_id()
    nueva_multa['usuario_id'] = usuario_id
    multas_sanciones_db.append(nueva_multa)
    
    return {"message": "Multa o sanción agregada exitosamente"}