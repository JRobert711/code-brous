from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random

app = FastAPI(title="KeyProject API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class Ciudadano(BaseModel):
    id: int
    nombre: str
    identificacion: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    fecha_creacion: datetime

class CiudadanoCreate(BaseModel):
    nombre: str
    identificacion: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class Drone(BaseModel):
    id: int
    modelo: str
    estado: str
    ubicacion: Optional[str] = None
    bateria: Optional[int] = None

class BiometricData(BaseModel):
    id: int
    ciudadano_id: int
    tipo: str
    datos: str
    fecha_registro: datetime

# ========== DATOS DE PRUEBA ==========

# Ciudadanos de prueba
ciudadanos_db = [
    Ciudadano(
        id=1,
        nombre="Ana García López",
        identificacion="12345678A",
        email="ana.garcia@email.com",
        telefono="+34 600 111 222",
        fecha_creacion=datetime.now() - timedelta(days=2)
    ),
    Ciudadano(
        id=2,
        nombre="Carlos Rodríguez Méndez",
        identificacion="87654321B",
        email="carlos.rodriguez@email.com",
        telefono="+34 600 333 444",
        fecha_creacion=datetime.now() - timedelta(days=5)
    ),
    Ciudadano(
        id=3,
        nombre="María Fernández Castro",
        identificacion="11223344C",
        email="maria.fernandez@email.com",
        telefono="+34 600 555 666",
        fecha_creacion=datetime.now() - timedelta(days=1)
    ),
    Ciudadano(
        id=4,
        nombre="Javier Martínez Ruiz",
        identificacion="44332211D",
        email="javier.martinez@email.com",
        telefono="+34 600 777 888",
        fecha_creacion=datetime.now() - timedelta(days=10)
    ),
    Ciudadano(
        id=5,
        nombre="Laura Sánchez Pérez",
        identificacion="55667788E",
        email="laura.sanchez@email.com",
        telefono="+34 600 999 000",
        fecha_creacion=datetime.now() - timedelta(days=15)
    )
]

# Drones de prueba
drones_db = [
    Drone(
        id=1,
        modelo="DJI Mavic 3",
        estado="activo",
        ubicacion="Zona Norte",
        bateria=85
    ),
    Drone(
        id=2,
        modelo="Autel Evo II",
        estado="activo", 
        ubicacion="Zona Centro",
        bateria=45
    ),
    Drone(
        id=3,
        modelo="DJI Phantom 4",
        estado="mantenimiento",
        ubicacion="Base Central",
        bateria=100
    ),
    Drone(
        id=4,
        modelo="Parrot Anafi",
        estado="activo",
        ubicacion="Zona Sur",
        bateria=20
    ),
    Drone(
        id=5,
        modelo="Yuneec Typhoon",
        estado="inactivo",
        ubicacion="Almacén",
        bateria=0
    )
]

# Datos biométricos de prueba
biometricos_db = [
    BiometricData(
        id=1,
        ciudadano_id=1,
        tipo="huella_digital",
        datos="template_001",
        fecha_registro=datetime.now() - timedelta(days=1)
    ),
    BiometricData(
        id=2,
        ciudadano_id=2,
        tipo="reconocimiento_facial",
        datos="template_002",
        fecha_registro=datetime.now() - timedelta(days=3)
    ),
    BiometricData(
        id=3,
        ciudadano_id=3,
        tipo="huella_digital",
        datos="template_003",
        fecha_registro=datetime.now() - timedelta(days=2)
    )
]

# ========== ENDPOINTS ==========

@app.get("/")
def root():
    return {
        "message": "🚀 KeyProject Backend funcionando",
        "version": "1.0",
        "modulos": ["Ciudadanos", "Drones", "Biometría"],
        "status": "operacional"
    }

# ========== CIUDADANOS ==========

@app.get("/api/ciudadanos", response_model=List[Ciudadano])
async def get_ciudadanos():
    """Obtener todos los ciudadanos"""
    return ciudadanos_db

@app.post("/api/ciudadanos", response_model=Ciudadano)
async def create_ciudadano(ciudadano: CiudadanoCreate):
    """Crear un nuevo ciudadano"""
    new_id = max([c.id for c in ciudadanos_db]) + 1 if ciudadanos_db else 1
    new_ciudadano = Ciudadano(
        id=new_id,
        nombre=ciudadano.nombre,
        identificacion=ciudadano.identificacion,
        email=ciudadano.email,
        telefono=ciudadano.telefono,
        fecha_creacion=datetime.now()
    )
    ciudadanos_db.append(new_ciudadano)
    return new_ciudadano

@app.put("/api/ciudadanos/{ciudadano_id}", response_model=Ciudadano)
async def update_ciudadano(ciudadano_id: int, ciudadano: CiudadanoCreate):
    """Actualizar un ciudadano existente"""
    for index, c in enumerate(ciudadanos_db):
        if c.id == ciudadano_id:
            updated_ciudadano = Ciudadano(
                id=ciudadano_id,
                nombre=ciudadano.nombre,
                identificacion=ciudadano.identificacion,
                email=ciudadano.email,
                telefono=ciudadano.telefono,
                fecha_creacion=ciudadanos_db[index].fecha_creacion
            )
            ciudadanos_db[index] = updated_ciudadano
            return updated_ciudadano
    raise HTTPException(status_code=404, detail="Ciudadano no encontrado")

@app.delete("/api/ciudadanos/{ciudadano_id}")
async def delete_ciudadano(ciudadano_id: int):
    """Eliminar un ciudadano"""
    for index, c in enumerate(ciudadanos_db):
        if c.id == ciudadano_id:
            ciudadanos_db.pop(index)
            return {"message": "Ciudadano eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Ciudadano no encontrado")

# ========== DRONES ==========

@app.get("/api/drones", response_model=List[Drone])
async def get_drones():
    """Obtener todos los drones"""
    return drones_db

@app.post("/api/drones", response_model=Drone)
async def create_drone(drone_data: dict):
    """Crear un nuevo drone"""
    new_id = max([d.id for d in drones_db]) + 1 if drones_db else 1
    new_drone = Drone(
        id=new_id,
        modelo=drone_data.get("modelo", "Desconocido"),
        estado=drone_data.get("estado", "inactivo"),
        ubicacion=drone_data.get("ubicacion"),
        bateria=drone_data.get("bateria", 0)
    )
    drones_db.append(new_drone)
    return new_drone

# ========== BIOMETRÍA ==========

@app.get("/api/biometria", response_model=List[BiometricData])
async def get_biometricos():
    """Obtener todos los registros biométricos"""
    return biometricos_db

@app.get("/api/biometria/{ciudadano_id}", response_model=List[BiometricData])
async def get_biometricos_ciudadano(ciudadano_id: int):
    """Obtener registros biométricos de un ciudadano específico"""
    return [b for b in biometricos_db if b.ciudadano_id == ciudadano_id]

# ========== DASHBOARD ==========

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    total_ciudadanos = len(ciudadanos_db)
    drones_activos = len([d for d in drones_db if d.estado == "activo"])
    total_drones = len(drones_db)
    registros_biometricos = len(biometricos_db)
    
    # Ciudadanos de la última semana
    una_semana_atras = datetime.now() - timedelta(days=7)
    ciudadanos_recientes = len([c for c in ciudadanos_db if c.fecha_creacion > una_semana_atras])
    
    return {
        "totalCiudadanos": total_ciudadanos,
        "dronesActivos": drones_activos,
        "totalDrones": total_drones,
        "registrosBiometricos": registros_biometricos,
        "ciudadanosRecientes": ciudadanos_recientes
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "data_samples": {
            "ciudadanos": len(ciudadanos_db),
            "drones": len(drones_db),
            "biometricos": len(biometricos_db)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)