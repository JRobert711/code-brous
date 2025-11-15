# backend/main.py - ACTUALIZAR CON ESTE CÓDIGO
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import base64
import os
import hashlib
from datetime import datetime

# Importar tus módulos
from database import db_manager
from models import *

app = FastAPI(title="IDN SV - Sistema de Identidad Digital")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de base de datos
def get_db():
    conn = db_manager.get_connection()
    try:
        yield conn
    finally:
        conn.close()

# Middleware para logs de seguridad
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    
    # Log de seguridad básico
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO security_logs (accion, descripcion, ip_address)
        VALUES (?, ?, ?)
    ''', (f"{request.method} {request.url.path}", "Acceso API", request.client.host))
    conn.commit()
    conn.close()
    
    return response

# Endpoints de Usuarios
@app.post("/api/usuarios", response_model=Usuario)
async def crear_usuario(usuario: UsuarioCreate, conn = Depends(get_db)):
    """Crear nuevo usuario"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (dui, nombres, apellidos, email, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            usuario.dui, 
            usuario.nombres, 
            usuario.apellidos, 
            usuario.email, 
            usuario.fecha_nacimiento
        ))
        conn.commit()
        
        # Obtener el usuario creado
        cursor.execute("SELECT * FROM usuarios WHERE id = LAST_INSERT_ROWID()")
        user_data = cursor.fetchone()
        
        return {
            "id": user_data[0],
            "dui": user_data[1],
            "nombres": user_data[2],
            "apellidos": user_data[3],
            "email": user_data[4],
            "fecha_nacimiento": user_data[5],
            "created_at": user_data[6]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")

@app.get("/api/usuarios/{dui}")
async def obtener_usuario(dui: str, conn = Depends(get_db)):
    """Obtener usuario por DUI"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, dui, nombres, apellidos, email, fecha_nacimiento, created_at
            FROM usuarios WHERE dui = ?
        ''', (dui,))
        
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "id": usuario[0],
            "dui": usuario[1],
            "nombres": usuario[2],
            "apellidos": usuario[3],
            "email": usuario[4],
            "fecha_nacimiento": usuario[5],
            "created_at": usuario[6]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo usuario: {str(e)}")

# Endpoints de Autenticación por Voz
@app.post("/api/voice/register")
async def register_voice(voice_data: VoiceRegisterRequest, conn = Depends(get_db)):
    """Registrar voz de usuario"""
    try:
        # Buscar usuario
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE dui = ?", (voice_data.dui,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear hash de voz (simulado por ahora)
        voice_hash = hashlib.sha256(voice_data.audio_data.encode()).hexdigest()
        
        # Guardar perfil de voz
        cursor.execute('''
            INSERT OR REPLACE INTO voice_profiles (usuario_id, voice_hash)
            VALUES (?, ?)
        ''', (usuario[0], voice_hash))
        
        conn.commit()
        
        return {"message": "Voz registrada exitosamente", "voice_hash": voice_hash}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando voz: {str(e)}")

@app.post("/api/voice/login")
async def voice_login(login_data: VoiceLoginRequest, conn = Depends(get_db)):
    """Autenticación por voz"""
    try:
        cursor = conn.cursor()
        
        # Buscar usuario
        cursor.execute("SELECT id FROM usuarios WHERE dui = ?", (login_data.dui,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar voz (simulación)
        voice_hash = hashlib.sha256(login_data.audio_data.encode()).hexdigest()
        
        cursor.execute('''
            SELECT voice_hash FROM voice_profiles 
            WHERE usuario_id = ? AND voice_hash = ?
        ''', (usuario[0], voice_hash))
        
        voice_profile = cursor.fetchone()
        
        if voice_profile:
            # Log de acceso exitoso
            cursor.execute('''
                INSERT INTO security_logs (usuario_id, accion, descripcion)
                VALUES (?, ?, ?)
            ''', (usuario[0], "LOGIN_VOICE_SUCCESS", "Autenticación por voz exitosa"))
            conn.commit()
            
            return {
                "authenticated": True,
                "usuario_id": usuario[0],
                "message": "Autenticación por voz exitosa"
            }
        else:
            # Log de intento fallido
            cursor.execute('''
                INSERT INTO security_logs (usuario_id, accion, descripcion)
                VALUES (?, ?, ?)
            ''', (usuario[0], "LOGIN_VOICE_FAILED", "Intento de autenticación por voz fallido"))
            conn.commit()
            
            return {
                "authenticated": False,
                "message": "Voz no reconocida"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# Endpoints de Drones
@app.get("/api/drones")
async def get_drones(conn = Depends(get_db)):
    """Obtener lista de drones"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nombre, estado, ubicacion_lat, ubicacion_lng, bateria, ultima_actualizacion
            FROM drones
        ''')
        
        drones = cursor.fetchall()
        return [
            {
                "id": drone[0],
                "nombre": drone[1],
                "estado": drone[2],
                "ubicacion_lat": drone[3],
                "ubicacion_lng": drone[4],
                "bateria": drone[5],
                "ultima_actualizacion": drone[6]
            }
            for drone in drones
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo drones: {str(e)}")

@app.get("/api/security/logs")
async def get_security_logs(conn = Depends(get_db)):
    """Obtener logs de seguridad"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT sl.id, u.dui, sl.accion, sl.descripcion, sl.ip_address, sl.created_at
            FROM security_logs sl
            LEFT JOIN usuarios u ON sl.usuario_id = u.id
            ORDER BY sl.created_at DESC
            LIMIT 50
        ''')
        
        logs = cursor.fetchall()
        return [
            {
                "id": log[0],
                "dui": log[1],
                "accion": log[2],
                "descripcion": log[3],
                "ip_address": log[4],
                "created_at": log[5]
            }
            for log in logs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo logs: {str(e)}")

# Mantener tus endpoints existentes
@app.get("/")
async def root():
    return {"message": "IDN SV API con Base de Datos funcionando!", "version": "2.0"}

@app.get("/docs")
async def get_docs():
    return {"message": "Documentación disponible en /docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)