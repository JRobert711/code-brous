# app/api/routes/drones.py
from fastapi import APIRouter, Depends
import sqlite3

router = APIRouter()

def get_db():
    conn = sqlite3.connect("idn_sv.db")
    try:
        yield conn
    finally:
        conn.close()

@router.get("/")
async def get_drones(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, estado, ubicacion_lat, ubicacion_lng, bateria FROM drones"
    )
    drones = cursor.fetchall()
    
    return [
        {
            "id": drone[0],
            "nombre": drone[1],
            "estado": drone[2],
            "ubicacion_lat": drone[3],
            "ubicacion_lng": drone[4],
            "bateria": drone[5]
        }
        for drone in drones
    ]