from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum

class SectorType(str, Enum):
    CIUDADANO = "ciudadano"
    MEDICO = "medico"
    EDUCATIVO = "educativo"
    JUDICIAL = "judicial"
    LABORAL = "laboral"
    SERVICIOS_SOCIALES = "servicios_sociales"
    ADMIN = "admin"

class NivelAcceso(int, Enum):
    CIUDADANO = 1
    SERVICIOS_SOCIALES = 2
    LABORAL = 3
    EDUCATIVO = 4
    JUDICIAL = 5
    MEDICO = 6
    ADMIN = 7

class PermisoType(str, Enum):
    # Permisos básicos
    LECTURA_PROPIA = "lectura_propia"
    ESCRITURA_PROPIA = "escritura_propia"
    
    # Permisos por módulo
    LECTURA_SALUD = "lectura_salud"
    ESCRITURA_SALUD = "escritura_salud"
    
    LECTURA_EDUCACION = "lectura_educacion"
    ESCRITURA_EDUCACION = "escritura_educacion"
    
    LECTURA_LABORAL = "lectura_laboral"
    ESCRITURA_LABORAL = "escritura_laboral"
    
    LECTURA_JUDICIAL = "lectura_judicial"
    ESCRITURA_JUDICIAL = "escritura_judicial"
    
    LECTURA_SERVICIOS_SOCIALES = "lectura_servicios_sociales"
    ESCRITURA_SERVICIOS_SOCIALES = "escritura_servicios_sociales"
    
    # Permisos administrativos
    LECTURA_GLOBAL = "lectura_global"
    ESCRITURA_GLOBAL = "escritura_global"

class UsuarioBase(BaseModel):
    dui: str
    nombres: str
    apellidos: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    sector: SectorType = SectorType.CIUDADANO
    nivel_acceso: NivelAcceso = NivelAcceso.CIUDADANO

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

# ========== MÓDULO SALUD ==========
class HistorialMedico(BaseModel):
    id: int
    usuario_id: int
    grupo_sanguineo: Optional[str] = None
    alergias: Optional[str] = None
    enfermedades_cronicas: Optional[str] = None
    discapacidades: Optional[str] = None

    class Config:
        from_attributes = True

class Vacuna(BaseModel):
    id: int
    usuario_id: int
    nombre: str
    fecha_aplicacion: date
    lote: Optional[str] = None
    centro_salud: str

    class Config:
        from_attributes = True

class Operacion(BaseModel):
    id: int
    usuario_id: int
    tipo_operacion: str
    fecha: date
    hospital: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class Medicamento(BaseModel):
    id: int
    usuario_id: int
    nombre: str
    dosis: str
    frecuencia: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    recetado_por: str

    class Config:
        from_attributes = True

# ========== MÓDULO EDUCACIÓN ==========
class TituloAcademico(BaseModel):
    id: int
    usuario_id: int
    nivel_educativo: str
    institucion: str
    titulo: str
    año_graduacion: int
    promedio: Optional[float] = None

    class Config:
        from_attributes = True

class Certificacion(BaseModel):
    id: int
    usuario_id: int
    nombre: str
    institucion: str
    fecha_emision: date
    fecha_expiracion: Optional[date] = None

    class Config:
        from_attributes = True

class CursoEspecializado(BaseModel):
    id: int
    usuario_id: int
    nombre_curso: str
    institucion: str
    horas: int
    fecha_completacion: date

    class Config:
        from_attributes = True

# ========== MÓDULO LABORAL ==========
class ExperienciaLaboral(BaseModel):
    id: int
    usuario_id: int
    empresa: str
    puesto: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    responsabilidades: Optional[str] = None
    salario_final: Optional[float] = None

    class Config:
        from_attributes = True

class HabilidadVerificada(BaseModel):
    id: int
    usuario_id: int
    habilidad: str
    nivel: str
    verificada_por: str
    fecha_verificacion: date

    class Config:
        from_attributes = True

class ContribucionISSS(BaseModel):
    id: int
    usuario_id: int
    empleador: str
    meses_cotizados: int
    ultima_contribucion: date
    monto_actual: Optional[float] = None

    class Config:
        from_attributes = True

# ========== MÓDULO JUDICIAL ==========
class AntecedentePenal(BaseModel):
    id: int
    usuario_id: int
    delito: str
    fecha_delito: date
    sentencia: str
    estado: str
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

class LicenciaConducir(BaseModel):
    id: int
    usuario_id: int
    categoria: str
    fecha_emision: date
    fecha_expiracion: date
    restricciones: Optional[str] = None
    puntos: int = 12

    class Config:
        from_attributes = True

class MultaSancion(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    motivo: str
    monto: float
    fecha: date
    estado: str

    class Config:
        from_attributes = True

# ========== MÓDULO SERVICIOS SOCIALES ==========
class Pension(BaseModel):
    id: int
    usuario_id: int
    tipo_pension: str
    monto_mensual: float
    fecha_inicio: date
    entidad_emisora: str

    class Config:
        from_attributes = True

class Subsidio(BaseModel):
    id: int
    usuario_id: int
    tipo_subsidio: str
    monto: float
    fecha_asignacion: date
    fecha_vencimiento: Optional[date] = None

    class Config:
        from_attributes = True

class AyudaEstatal(BaseModel):
    id: int
    usuario_id: int
    programa: str
    beneficio: str
    fecha_asignacion: date
    vigente: bool = True

    class Config:
        from_attributes = True

# ========== MODELO COMPLETO DEL USUARIO ==========
class UsuarioCompleto(Usuario):
    # Salud
    historial_medico: Optional[HistorialMedico] = None
    vacunas: List[Vacuna] = []
    operaciones: List[Operacion] = []
    medicamentos: List[Medicamento] = []
    
    # Educación
    titulos_academicos: List[TituloAcademico] = []
    certificaciones: List[Certificacion] = []
    cursos_especializados: List[CursoEspecializado] = []
    
    # Laboral
    experiencia_laboral: List[ExperienciaLaboral] = []
    habilidades_verificadas: List[HabilidadVerificada] = []
    contribuciones_isss: List[ContribucionISSS] = []
    
    # Judicial
    antecedentes_penales: List[AntecedentePenal] = []
    licencias_conducir: List[LicenciaConducir] = []
    multas_sanciones: List[MultaSancion] = []
    
    # Servicios Sociales
    pensiones: List[Pension] = []
    subsidios: List[Subsidio] = []
    ayudas_estatales: List[AyudaEstatal] = []
    
    permisos: List[PermisoType] = []

class VoiceLoginRequest(BaseModel):
    dui: str
    audio_data: str

class VoiceRegisterRequest(BaseModel):
    dui: str
    audio_data: str

class SecurityLog(BaseModel):
    id: int
    usuario_id: Optional[int]
    accion: str
    descripcion: str
    modulo_afectado: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        
        # ========== MODELOS DE AUTENTICACIÓN ==========
from pydantic import validator
import re

class LoginRequest(BaseModel):
    dui: str
    password: str
    captcha_token: str

    @validator('dui')
    def validate_dui(cls, v):
        if not re.match(r'^\d{8}-\d$', v):
            raise ValueError('Formato DUI inválido. Use: 12345678-9')
        return v

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario
    permisos: List[PermisoType] = []

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario
    permisos: List[PermisoType] = []

class MessageResponse(BaseModel):
    message: str

# Modelo para login con documento alternativo
class DocumentLoginRequest(BaseModel):
    document_type: str
    document_value: str
    password: str
    captcha_token: str