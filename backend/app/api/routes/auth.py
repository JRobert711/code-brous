# app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import hashlib
import sqlite3

router = APIRouter()

class VoiceLoginRequest(BaseModel):
    dui: str
    audio_data: str

class VoiceRegisterRequest(BaseModel):
    dui: str
    audio_data: str

# Conexión simple a SQLite
def get_db():
    conn = sqlite3.connect("idn_sv.db")
    try:
        yield conn
    finally:
        conn.close()

@router.post("/voice-login")
async def voice_login(login_data: VoiceLoginRequest, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    
    # Buscar usuario
    cursor.execute("SELECT id FROM usuarios WHERE dui = ?", (login_data.dui,))
    usuario = cursor.fetchone()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar voz (hash simulado)
    voice_hash = hashlib.sha256(login_data.audio_data.encode()).hexdigest()
    
    cursor.execute(
        "SELECT id FROM voice_profiles WHERE usuario_id = ? AND voice_hash = ?",
        (usuario[0], voice_hash)
    )
    voice_profile = cursor.fetchone()
    
    if voice_profile:
        return {"authenticated": True, "usuario_id": usuario[0]}
    else:
        return {"authenticated": False}

@router.post("/register-voice")
async def register_voice(voice_data: VoiceRegisterRequest, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM usuarios WHERE dui = ?", (voice_data.dui,))
    usuario = cursor.fetchone()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    voice_hash = hashlib.sha256(voice_data.audio_data.encode()).hexdigest()
    
    cursor.execute(
        "INSERT OR REPLACE INTO voice_profiles (usuario_id, voice_hash) VALUES (?, ?)",
        (usuario[0], voice_hash)
    )
    conn.commit()
    
    return {"message": "Voz registrada exitosamente"}