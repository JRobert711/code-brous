# app/api/routes/ciudadanos.py
from fastapi import APIRouter, HTTPException, Depends
import sqlite3

router = APIRouter()

def get_db():
    conn = sqlite3.connect("idn_sv.db")
    try:
        yield conn
    finally:
        conn.close()

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