from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.models import TituloAcademico, Certificacion, CursoEspecializado, Usuario
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import get_current_user
from backend.app.shared_data import titulos_academicos_db, certificaciones_db, cursos_especializados_db, get_next_id

router = APIRouter(prefix="/educacion", tags=["educacion"])

@router.get("/{usuario_id}/titulos", response_model=List[TituloAcademico])
async def obtener_titulos(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener títulos académicos de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'educacion'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al módulo de educación"
        )
    
    titulos = [t for t in titulos_academicos_db if t['usuario_id'] == usuario_id]
    return [TituloAcademico(**t) for t in titulos]

@router.post("/{usuario_id}/titulos")
async def agregar_titulo(
    usuario_id: int,
    titulo: TituloAcademico,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nuevo título académico"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'educacion'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar títulos académicos"
        )
    
    nuevo_titulo = titulo.dict()
    nuevo_titulo['id'] = get_next_id()
    nuevo_titulo['usuario_id'] = usuario_id
    titulos_academicos_db.append(nuevo_titulo)
    
    return {"message": "Título académico agregado exitosamente"}

@router.get("/{usuario_id}/certificaciones", response_model=List[Certificacion])
async def obtener_certificaciones(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener certificaciones de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'educacion'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a certificaciones")
    
    certificaciones = [c for c in certificaciones_db if c['usuario_id'] == usuario_id]
    return [Certificacion(**c) for c in certificaciones]

@router.post("/{usuario_id}/certificaciones")
async def agregar_certificacion(
    usuario_id: int,
    certificacion: Certificacion,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nueva certificación"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'educacion'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar certificaciones")
    
    nueva_certificacion = certificacion.dict()
    nueva_certificacion['id'] = get_next_id()
    nueva_certificacion['usuario_id'] = usuario_id
    certificaciones_db.append(nueva_certificacion)
    
    return {"message": "Certificación agregada exitosamente"}

@router.get("/{usuario_id}/cursos", response_model=List[CursoEspecializado])
async def obtener_cursos(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener cursos especializados de un usuario"""
    if not AuthorizationService.puede_acceder_modulo(current_user, 'educacion'):
        raise HTTPException(status_code=403, detail="Sin permisos para acceder a cursos")
    
    cursos = [c for c in cursos_especializados_db if c['usuario_id'] == usuario_id]
    return [CursoEspecializado(**c) for c in cursos]

@router.post("/{usuario_id}/cursos")
async def agregar_curso(
    usuario_id: int,
    curso: CursoEspecializado,
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar nuevo curso especializado"""
    if not AuthorizationService.puede_editar_modulo(current_user, 'educacion'):
        raise HTTPException(status_code=403, detail="Sin permisos para agregar cursos")
    
    nuevo_curso = curso.dict()
    nuevo_curso['id'] = get_next_id()
    nuevo_curso['usuario_id'] = usuario_id
    cursos_especializados_db.append(nuevo_curso)
    
    return {"message": "Curso especializado agregado exitosamente"}