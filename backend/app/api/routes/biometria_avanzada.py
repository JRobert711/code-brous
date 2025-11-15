# app/api/routes/biometria_avanzada.py
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import sqlite3
import cv2
import numpy as np
import hashlib
from datetime import datetime
import os

router = APIRouter()

def get_db():
    conn = sqlite3.connect("idn_sv.db")
    try:
        yield conn
    finally:
        conn.close()

class ImageProcessor:
    """Procesador de imágenes con OpenCV"""
    
    @staticmethod
    def extract_image_features(image_data: bytes):
        """Extraer características de imagen usando OpenCV"""
        try:
            # Convertir bytes a imagen OpenCV
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return None
            
            # Extraer características básicas
            height, width, channels = image.shape
            image_hash = hashlib.sha256(image_data).hexdigest()
            
            # Convertir a escala de grises para análisis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Características de la imagen
            features = {
                "hash": image_hash,
                "dimensions": f"{width}x{height}",
                "file_size": len(image_data),
                "mean_brightness": np.mean(gray),
                "contrast": np.std(gray),
                "timestamp": datetime.now().isoformat()
            }
            
            # Detectar caras (simulación - sin face_recognition)
            # En producción usaríamos face_recognition aquí
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            features["faces_detected"] = len(faces)
            features["face_locations"] = [{"x": x, "y": y, "w": w, "h": h} for (x, y, w, h) in faces]
            
            return features
            
        except Exception as e:
            print(f"Error procesando imagen: {e}")
            return None

image_processor = ImageProcessor()

@router.post("/analyze-image")
async def analyze_image(image_file: UploadFile = File(...)):
    """Analizar imagen con OpenCV"""
    try:
        if not image_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Archivo debe ser una imagen")
        
        image_data = await image_file.read()
        features = image_processor.extract_image_features(image_data)
        
        if not features:
            raise HTTPException(status_code=400, detail="Error procesando imagen")
        
        return {
            "analysis": "Completado con OpenCV",
            "features": features,
            "message": f"✅ Imagen analizada: {features['faces_detected']} caras detectadas"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando imagen: {str(e)}")

@router.get("/system-stats")
async def get_system_stats(conn: sqlite3.Connection = Depends(get_db)):
    """Estadísticas avanzadas del sistema"""
    cursor = conn.cursor()
    
    # Estadísticas de usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT usuario_id) FROM voice_profiles")
    usuarios_con_voz = cursor.fetchone()[0]
    
    # Actividad reciente
    cursor.execute('''
        SELECT accion, COUNT(*) as count 
        FROM security_logs 
        WHERE created_at >= datetime('now', '-1 day')
        GROUP BY accion
    ''')
    actividad_reciente = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Uso del sistema
    cursor.execute("SELECT COUNT(*) FROM security_logs")
    total_logs = cursor.fetchone()[0]
    
    return {
        "estadisticas_avanzadas": {
            "total_usuarios": total_usuarios,
            "usuarios_biometria": usuarios_con_voz,
            "cobertura_biometria": f"{(usuarios_con_voz/total_usuarios*100):.1f}%" if total_usuarios > 0 else "0%",
            "total_eventos_seguridad": total_logs
        },
        "actividad_24h": actividad_reciente,
        "tecnologias_activas": [
            "FastAPI Backend",
            "SQLite Database", 
            "SpeechRecognition",
            "OpenCV Image Processing",
            "JWT Authentication"
        ],
        "timestamp": datetime.now().isoformat()
    }