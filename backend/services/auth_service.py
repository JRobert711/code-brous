from typing import List, Dict, Any, Optional
from ..models.models import SectorType, PermisoType, NivelAcceso, Usuario
from backend.app.middleware.auth_middleware import obtener_usuario_por_id

class AuthorizationService:
    # Mapeo de sector a nivel de acceso
    SECTOR_TO_NIVEL = {
        SectorType.CIUDADANO: NivelAcceso.CIUDADANO,
        SectorType.SERVICIOS_SOCIALES: NivelAcceso.SERVICIOS_SOCIALES,
        SectorType.LABORAL: NivelAcceso.LABORAL,
        SectorType.EDUCATIVO: NivelAcceso.EDUCATIVO,
        SectorType.JUDICIAL: NivelAcceso.JUDICIAL,
        SectorType.MEDICO: NivelAcceso.MEDICO,
        SectorType.ADMIN: NivelAcceso.ADMIN
    }

    # Permisos por nivel de acceso (pirámide)
    PERMISOS_POR_NIVEL = {
        NivelAcceso.CIUDADANO: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA
        ],
        NivelAcceso.SERVICIOS_SOCIALES: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA,
            PermisoType.LECTURA_SERVICIOS_SOCIALES,
            PermisoType.ESCRITURA_SERVICIOS_SOCIALES
        ],
        NivelAcceso.LABORAL: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA,
            PermisoType.LECTURA_LABORAL,
            PermisoType.ESCRITURA_LABORAL
        ],
        NivelAcceso.EDUCATIVO: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA,
            PermisoType.LECTURA_EDUCACION,
            PermisoType.ESCRITURA_EDUCACION
        ],
        NivelAcceso.JUDICIAL: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA,
            PermisoType.LECTURA_JUDICIAL,
            PermisoType.ESCRITURA_JUDICIAL
        ],
        NivelAcceso.MEDICO: [
            PermisoType.LECTURA_PROPIA,
            PermisoType.ESCRITURA_PROPIA,
            PermisoType.LECTURA_SALUD,
            PermisoType.ESCRITURA_SALUD
        ],
        NivelAcceso.ADMIN: [
            PermisoType.LECTURA_GLOBAL,
            PermisoType.ESCRITURA_GLOBAL
        ]
    }

    @classmethod
    def get_nivel_acceso(cls, usuario: Usuario) -> NivelAcceso:
        """Obtener nivel de acceso del usuario"""
        return cls.SECTOR_TO_NIVEL.get(usuario.sector, NivelAcceso.CIUDADANO)

    @classmethod
    def get_permisos_usuario(cls, usuario: Usuario) -> List[PermisoType]:
        """Obtener permisos basados en el nivel de acceso"""
        nivel = cls.get_nivel_acceso(usuario)
        return cls.PERMISOS_POR_NIVEL.get(nivel, [])

    @classmethod
    def puede_acceder_modulo(cls, usuario: Usuario, modulo: str) -> bool:
        """Verificar si un usuario puede acceder a un módulo específico"""
        permisos = cls.get_permisos_usuario(usuario)
        
        modulos_permisos = {
            'salud': [PermisoType.LECTURA_SALUD, PermisoType.LECTURA_GLOBAL],
            'educacion': [PermisoType.LECTURA_EDUCACION, PermisoType.LECTURA_GLOBAL],
            'laboral': [PermisoType.LECTURA_LABORAL, PermisoType.LECTURA_GLOBAL],
            'judicial': [PermisoType.LECTURA_JUDICIAL, PermisoType.LECTURA_GLOBAL],
            'servicios_sociales': [PermisoType.LECTURA_SERVICIOS_SOCIALES, PermisoType.LECTURA_GLOBAL]
        }
        
        return any(permiso in permisos for permiso in modulos_permisos.get(modulo, []))

    @classmethod
    def puede_editar_modulo(cls, usuario: Usuario, modulo: str) -> bool:
        """Verificar si un usuario puede editar un módulo específico"""
        permisos = cls.get_permisos_usuario(usuario)
        
        modulos_permisos = {
            'salud': [PermisoType.ESCRITURA_SALUD, PermisoType.ESCRITURA_GLOBAL],
            'educacion': [PermisoType.ESCRITURA_EDUCACION, PermisoType.ESCRITURA_GLOBAL],
            'laboral': [PermisoType.ESCRITURA_LABORAL, PermisoType.ESCRITURA_GLOBAL],
            'judicial': [PermisoType.ESCRITURA_JUDICIAL, PermisoType.ESCRITURA_GLOBAL],
            'servicios_sociales': [PermisoType.ESCRITURA_SERVICIOS_SOCIALES, PermisoType.ESCRITURA_GLOBAL]
        }
        
        return any(permiso in permisos for permiso in modulos_permisos.get(modulo, []))

    @classmethod
    def puede_ver_usuario(cls, usuario_actual: Usuario, usuario_target_id: int) -> bool:
        """Verificar si un usuario puede ver la información de otro"""
        # Siempre puede verse a sí mismo
        if usuario_target_id == usuario_actual.id:
            return True
        
        # Admin puede ver a todos
        if usuario_actual.sector == SectorType.ADMIN:
            return True
        
        # Obtener usuario target
        usuario_target = obtener_usuario_por_id(usuario_target_id)
        if not usuario_target:
            return False
        
        # Usuarios con nivel superior pueden ver a inferiores
        nivel_actual = cls.get_nivel_acceso(usuario_actual)
        nivel_target = cls.get_nivel_acceso(usuario_target)
        
        return nivel_actual >= nivel_target

    @classmethod
    def filtrar_datos_usuario(cls, usuario_actual: Usuario, datos_completos: Dict[str, Any]) -> Dict[str, Any]:
        """Filtrar datos según permisos del usuario actual"""
        datos_filtrados = {
            'id': datos_completos['id'],
            'dui': datos_completos['dui'],
            'nombres': datos_completos['nombres'],
            'apellidos': datos_completos['apellidos'],
            'sector': datos_completos['sector']
        }

        # Información básica para niveles superiores
        if cls.get_nivel_acceso(usuario_actual) > NivelAcceso.CIUDADANO:
            datos_filtrados.update({
                'email': datos_completos.get('email'),
                'telefono': datos_completos.get('telefono'),
                'fecha_nacimiento': datos_completos.get('fecha_nacimiento'),
                'direccion': datos_completos.get('direccion')
            })

        # Filtrar módulos según permisos
        modulos = {
            'salud': ['historial_medico', 'vacunas', 'operaciones', 'medicamentos'],
            'educacion': ['titulos_academicos', 'certificaciones', 'cursos_especializados'],
            'laboral': ['experiencia_laboral', 'habilidades_verificadas', 'contribuciones_isss'],
            'judicial': ['antecedentes_penales', 'licencias_conducir', 'multas_sanciones'],
            'servicios_sociales': ['pensiones', 'subsidios', 'ayudas_estatales']
        }

        for modulo, campos in modulos.items():
            if cls.puede_acceder_modulo(usuario_actual, modulo):
                for campo in campos:
                    if campo in datos_completos:
                        datos_filtrados[campo] = datos_completos[campo]

        return datos_filtrados

    @classmethod
    def verificar_permiso(cls, usuario: Usuario, permiso_requerido: PermisoType) -> bool:
        """Verificar si un usuario tiene un permiso específico"""
        return permiso_requerido in cls.get_permisos_usuario(usuario)