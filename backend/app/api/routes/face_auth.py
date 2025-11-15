# app/api/routes/face_auth.py
import cv2
import face_recognition
import numpy as np
import sqlite3
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

class FaceAuthService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_ids = []
        self.load_faces_from_db()
    
    def load_faces_from_db(self):
        """Cargar rostros conocidos desde la base de datos"""
        conn = sqlite3.connect("idn_sv.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario_id, face_encoding FROM face_profiles")
        faces = cursor.fetchall()
        
        for face in faces:
            # Convertir string de vuelta a numpy array
            encoding = np.fromstring(face[1], sep=',')
            self.known_face_encodings.append(encoding)
            self.known_face_ids.append(face[0])
        
        conn.close()
    
    def register_face(self, image_data: bytes, user_id: int):
        """Registrar nuevo rostro"""
        # Convertir bytes a imagen
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convertir BGR a RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        face_encodings = face_recognition.face_encodings(rgb_image)
        
        if len(face_encodings) == 0:
            return False
        
        # Guardar en base de datos
        conn = sqlite3.connect("idn_sv.db")
        cursor = conn.cursor()
        
        encoding_str = ','.join(map(str, face_encodings[0]))
        cursor.execute(
            "INSERT OR REPLACE INTO face_profiles (usuario_id, face_encoding) VALUES (?, ?)",
            (user_id, encoding_str)
        )
        conn.commit()
        conn.close()
        
        # Actualizar cache
        self.known_face_encodings.append(face_encodings[0])
        self.known_face_ids.append(user_id)
        
        return True
    
    def verify_face(self, image_data: bytes):
        """Verificar rostro"""
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        face_encodings = face_recognition.face_encodings(rgb_image)
        
        if len(face_encodings) == 0:
            return None
        
        # Comparar con rostros conocidos
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings[0])
        
        if True in matches:
            first_match_index = matches.index(True)
            return self.known_face_ids[first_match_index]
        
        return None

face_service = FaceAuthService()

@router.post("/register-face")
async def register_face(user_id: int, file: UploadFile = File(...)):
    """Registrar rostro de usuario"""
    image_data = await file.read()
    success = face_service.register_face(image_data, user_id)
    
    if success:
        return {"message": "Rostro registrado exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se detectó ningún rostro")

@router.post("/verify-face")
async def verify_face(file: UploadFile = File(...)):
    """Verificar rostro"""
    image_data = await file.read()
    user_id = face_service.verify_face(image_data)
    
    if user_id:
        return {"authenticated": True, "user_id": user_id}
    else:
        return {"authenticated": False}