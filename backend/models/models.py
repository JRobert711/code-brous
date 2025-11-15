# backend/models/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class UsuarioBase(BaseModel):
    dui: str
    nombres: str
    apellidos: str
    email: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VoiceLoginRequest(BaseModel):
    dui: str
    audio_data: str

class VoiceRegisterRequest(BaseModel):
    dui: str
    audio_data: str

class Drone(BaseModel):
    id: int
    nombre: str
    estado: str
    ubicacion_lat: float
    ubicacion_lng: float
    bateria: int
    ultima_actualizacion: datetime

    class Config:
        from_attributes = True

class SecurityLog(BaseModel):
    id: int
    usuario_id: Optional[int]
    accion: str
    descripcion: str
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True