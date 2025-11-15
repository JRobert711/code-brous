# app/api/routes/ciudadanos.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date
import sqlite3

router = APIRouter()

# Modelo para registro de ciudadanos
class CiudadanoCreate(BaseModel):
    dui: str
    nombres: str
    apellidos: str
    email: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

def get_db():
    conn = sqlite3.connect("idn_sv.db")
    try:
        yield conn
    finally:
        conn.close()

@router.post("/")
async def crear_ciudadano(
    ciudadano: CiudadanoCreate, 
    conn: sqlite3.Connection = Depends(get_db)
):
    """Registrar nuevo ciudadano en el sistema"""
    try:
        cursor = conn.cursor()
        
        # Verificar si el DUI ya existe
        cursor.execute("SELECT id FROM usuarios WHERE dui = ?", (ciudadano.dui,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El DUI ya está registrado")
        
        # Insertar nuevo ciudadano
        cursor.execute('''
            INSERT INTO usuarios (dui, nombres, apellidos, email, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            ciudadano.dui,
            ciudadano.nombres,
            ciudadano.apellidos,
            ciudadano.email,
            ciudadano.fecha_nacimiento
        ))
        
        # Obtener el ID del nuevo usuario
        user_id = cursor.lastrowid
        
        # Registrar en logs de seguridad
        cursor.execute('''
            INSERT INTO security_logs (usuario_id, accion, descripcion)
            VALUES (?, ?, ?)
        ''', (user_id, "USER_REGISTER", f"Usuario {ciudadano.dui} registrado en el sistema"))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Ciudadano registrado exitosamente",
            "user_id": user_id,
            "ciudadano": {
                "dui": ciudadano.dui,
                "nombres": ciudadano.nombres,
                "apellidos": ciudadano.apellidos,
                "email": ciudadano.email
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando ciudadano: {str(e)}")

# ... (mantener los endpoints existentes de get_ciudadano y get_all_ciudadanos)

@router.get("/{dui}")
async def get_ciudadano(dui: str, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, dui, nombres, apellidos, email, fecha_nacimiento FROM usuarios WHERE dui = ?",
        (dui,)
    )
    usuario = cursor.fetchone()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": usuario[0],
        "dui": usuario[1],
        "nombres": usuario[2],
        "apellidos": usuario[3],
        "email": usuario[4],
        "fecha_nacimiento": usuario[5]
    }