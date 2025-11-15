"""
Archivo para compartir datos entre diferentes routers
"""
from backend.models.models import Usuario

# ========== BASES DE DATOS DE USUARIOS ==========
usuarios_db = []
next_id = 6  # Empezar después de los usuarios de prueba

# ========== MÓDULO SALUD ==========
historial_medico_db = []
vacunas_db = []
operaciones_db = []
medicamentos_db = []

# ========== MÓDULO EDUCACIÓN ==========
titulos_academicos_db = []
certificaciones_db = []
cursos_especializados_db = []

# ========== MÓDULO LABORAL ==========
experiencia_laboral_db = []
habilidades_verificadas_db = []
contribuciones_isss_db = []

# ========== MÓDULO JUDICIAL ==========
antecedentes_penales_db = []
licencias_conducir_db = []
multas_sanciones_db = []

# ========== MÓDULO SERVICIOS SOCIALES ==========
pensiones_db = []
subsidios_db = []
ayudas_estatales_db = []

# ========== IDs GLOBALES ==========
global_next_id = 1000

def get_next_id():
    """Obtener el siguiente ID global"""
    global global_next_id
    current_id = global_next_id
    global_next_id += 1
    return current_id

def inicializar_datos_prueba():
    """Inicializar algunos datos de prueba para desarrollo"""
    from datetime import date, datetime
    
    # Datos de salud de prueba
    historial_medico_db.append({
        'id': get_next_id(),
        'usuario_id': 1,
        'grupo_sanguineo': 'O+',
        'alergias': 'Penicilina, Polvo',
        'enfermedades_cronicas': 'Ninguna',
        'discapacidades': 'Ninguna'
    })
    
    # Datos educativos de prueba
    titulos_academicos_db.append({
        'id': get_next_id(),
        'usuario_id': 1,
        'nivel_educativo': 'Universitario',
        'institucion': 'Universidad de El Salvador',
        'titulo': 'Ingeniero en Sistemas',
        'año_graduacion': 2020,
        'promedio': 8.5
    })
    
    # Datos laborales de prueba
    experiencia_laboral_db.append({
        'id': get_next_id(),
        'usuario_id': 1,
        'empresa': 'Tech Solutions SA',
        'puesto': 'Desarrollador Senior',
        'fecha_inicio': date(2021, 1, 15),
        'fecha_fin': None,
        'responsabilidades': 'Desarrollo de aplicaciones web',
        'salario_final': 2500.00
    })
    
    # Datos judiciales de prueba
    licencias_conducir_db.append({
        'id': get_next_id(),
        'usuario_id': 1,
        'categoria': 'B',
        'fecha_emision': date(2022, 5, 10),
        'fecha_expiracion': date(2027, 5, 10),
        'restricciones': 'Uso de lentes',
        'puntos': 12
    })
    
    # Datos de servicios sociales de prueba
    subsidios_db.append({
        'id': get_next_id(),
        'usuario_id': 1,
        'tipo_subsidio': 'Alimentación',
        'monto': 150.00,
        'fecha_asignacion': date(2024, 1, 1),
        'fecha_vencimiento': date(2024, 12, 31)
    })

# Ejecutar inicialización al importar
inicializar_datos_prueba()