from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.models import HistorialMedico, Vacuna, Operacion, Medicamento, Usuario
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import historial_medico_db, vacunas_db, operaciones_db, medicamentos_db, get_next_id

router = APIRouter(prefix="/salud", tags=["salud"])

@router.get("/{usuario_id}/historial", response_model=HistorialMedico)
async def obtener_historial_medico(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener historial médico de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'salud'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al módulo de salud"
        )
    
    historial = next((h for h in historial_medico_db if h.usuario_id == usuario_id), None)
    if not historial:
        # Crear un historial vacío si no existe
        historial_vacio = HistorialMedico(
            id=get_next_id(),
            usuario_id=usuario_id,
            grupo_sanguineo="No especificado",
            alergias="Ninguna conocida",
            enfermedades_cronicas="Ninguna",
            discapacidades="Ninguna"
        )
        return historial_vacio
    
    return historial

@router.put("/{usuario_id}/historial")
async def actualizar_historial_medico(
    usuario_id: int,
    historial: HistorialMedico,
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar historial médico"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'salud'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar historiales médicos"
        )
    
    # Buscar si ya existe
    existing_index = next((i for i, h in enumerate(historial_medico_db) 
                          if h.usuario_id == usuario_id), None)
    
    if existing_index is not None:
        historial_medico_db[existing_index] = historial
    else:
        historial.id = get_next_id()
        historial_medico_db.append(historial)
    
    return {"message": "Historial médico actualizado exitosamente"}

@router.get("/{usuario_id}/vacunas", response_model=List[Vacuna])
async def obtener_vacunas(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener vacunas de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'salud'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a vacunas")
    
    vacunas = [v for v in vacunas_db if v.usuario_id == usuario_id]
    return vacunas

@router.post("/{usuario_id}/vacunas")
async def agregar_vacuna(
    usuario_id: int,
    vacuna: Vacuna,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva vacuna"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'salud'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar vacunas")
    
    vacuna.id = get_next_id()
    vacuna.usuario_id = usuario_id
    vacunas_db.append(vacuna)
    
    return {"message": "Vacuna agregada exitosamente"}

@router.get("/{usuario_id}/operaciones", response_model=List[Operacion])
async def obtener_operaciones(usuario_id: int, current_user: Usuario = Depends(get_current_user)):
    """Obtener operaciones de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'salud'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a operaciones")
    
    return [o for o in operaciones_db if o.usuario_id == usuario_id]

@router.get("/{usuario_id}/medicamentos", response_model=List[Medicamento])
async def obtener_medicamentos(usuario_id: int, current_user: Usuario = Depends(get_current_user)):
    """Obtener medicamentos de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'salud'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a medicamentos")
    
    return [m for m in medicamentos_db if m.usuario_id == usuario_id]