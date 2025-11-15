# backend/app/routes/facial_symmetry.py
import cv2
import math
import base64
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import logging
import json

router = APIRouter(prefix="/facial-symmetry", tags=["Facial Symmetry Analysis"])

logger = logging.getLogger(__name__)

class FacialSymmetryAnalysis:
    def __init__(self):
        # Cargar clasificadores HAAR
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.nose_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_mcs_nose.xml'
            )
            self.mouth_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_mcs_mouth.xml'
            )
            
            # Verificar que los clasificadores se cargaron correctamente
            if (self.face_cascade.empty() or self.eye_cascade.empty() or 
                self.nose_cascade.empty() or self.mouth_cascade.empty()):
                raise Exception("No se pudieron cargar los clasificadores HAAR")
                
        except Exception as e:
            logger.error(f"Error cargando clasificadores: {e}")
            raise

        self.is_running = False
        self.cap = None
        
        # Configuración de colores
        self.colors = {
            'face': (0, 255, 0),        # Verde
            'eyes': (255, 0, 0),        # Azul
            'nose': (0, 255, 255),      # Amarillo
            'mouth': (0, 0, 255),       # Rojo
            'center': (255, 255, 255),  # Blanco
            'symmetry_line': (255, 0, 255),
            'text': (200, 200, 200)
        }

    def detect_facial_features(self, gray, face_roi):
        """Detectar características faciales"""
        x, y, w, h = face_roi
        features = {'eyes': [], 'nose': [], 'mouth': []}
        
        try:
            # Detectar ojos
            eyes = self.eye_cascade.detectMultiScale(gray[y:y+h, x:x+w], 1.1, 5)
            for (ex, ey, ew, eh) in eyes:
                features['eyes'].append((x + ex, y + ey, ew, eh))
            
            # Detectar nariz
            noses = self.nose_cascade.detectMultiScale(gray[y:y+h, x:x+w], 1.1, 5)
            for (nx, ny, nw, nh) in noses:
                features['nose'].append((x + nx, y + ny, nw, nh))
            
            # Detectar boca
            mouth_roi_y = int(y + h * 0.6)
            mouth_roi_h = int(h * 0.4)
            mouths = self.mouth_cascade.detectMultiScale(
                gray[mouth_roi_y:mouth_roi_y+mouth_roi_h, x:x+w], 1.1, 5
            )
            for (mx, my, mw, mh) in mouths:
                features['mouth'].append((x + mx, mouth_roi_y + my, mw, mh))
        except Exception as e:
            logger.error(f"Error detectando características faciales: {e}")
        
        return features

    def calculate_symmetry_score(self, features, face_center_x):
        """Calcular puntuación de simetría"""
        if not features['eyes']:
            return 0
        
        symmetry_scores = []
        
        try:
            # Simetría de ojos
            if len(features['eyes']) >= 2:
                eyes = sorted(features['eyes'], key=lambda e: e[0])
                left_eye = eyes[0]
                right_eye = eyes[1]
                
                left_center_x = left_eye[0] + left_eye[2] // 2
                right_center_x = right_eye[0] + right_eye[2] // 2
                
                left_dist = abs(left_center_x - face_center_x)
                right_dist = abs(right_center_x - face_center_x)
                
                if left_dist + right_dist > 0:
                    eye_symmetry = 100 * (1 - abs(left_dist - right_dist) / (left_dist + right_dist))
                    symmetry_scores.append(eye_symmetry)
            
            # Simetría de nariz
            if features['nose']:
                nose = features['nose'][0]
                nose_center_x = nose[0] + nose[2] // 2
                nose_symmetry = 100 * (1 - abs(nose_center_x - face_center_x) / (face_center_x))
                symmetry_scores.append(nose_symmetry * 0.5)
            
            # Simetría de boca
            if features['mouth']:
                mouth = features['mouth'][0]
                mouth_center_x = mouth[0] + mouth[2] // 2
                mouth_symmetry = 100 * (1 - abs(mouth_center_x - face_center_x) / (face_center_x))
                symmetry_scores.append(mouth_symmetry * 0.3)
        except Exception as e:
            logger.error(f"Error calculando simetría: {e}")
        
        return sum(symmetry_scores) / len(symmetry_scores) if symmetry_scores else 0

    def draw_analysis(self, frame, face_roi, features, symmetry_score):
        """Dibujar análisis en el frame"""
        try:
            x, y, w, h = face_roi
            face_center_x = x + w // 2
            
            # Dibujar rectángulo del rostro
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.colors['face'], 2)
            
            # Línea central
            cv2.line(frame, (face_center_x, y), (face_center_x, y + h), self.colors['center'], 2)
            
            # Dibujar características
            for (ex, ey, ew, eh) in features['eyes']:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), self.colors['eyes'], 2)
                eye_center_x = ex + ew // 2
                cv2.line(frame, (eye_center_x, ey), (eye_center_x, ey + eh), self.colors['symmetry_line'], 1)
            
            for (nx, ny, nw, nh) in features['nose']:
                cv2.rectangle(frame, (nx, ny), (nx + nw, ny + nh), self.colors['nose'], 2)
            
            for (mx, my, mw, mh) in features['mouth']:
                cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), self.colors['mouth'], 2)
            
            # Información de simetría
            cv2.rectangle(frame, (10, 10), (400, 120), (48, 56, 69), -1)
            cv2.rectangle(frame, (10, 10), (400, 120), self.colors['center'], 2)
            
            cv2.putText(frame, "ANALISIS DE SIMETRIA FACIAL", 
                       (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['text'], 2)
            cv2.putText(frame, f"Puntuacion: {symmetry_score:.1f}%", 
                       (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['text'], 2)
            
            interpretation, color = self.get_interpretation(symmetry_score)
            cv2.putText(frame, f"Interpretacion: {interpretation}", 
                       (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        except Exception as e:
            logger.error(f"Error dibujando análisis: {e}")
        
        return frame

    def get_interpretation(self, score):
        """Obtener interpretación del score"""
        if score >= 85: return "EXCELENTE SIMETRÍA", (0, 200, 0)
        elif score >= 75: return "BUENA SIMETRÍA", (0, 200, 0)
        elif score >= 65: return "SIMETRÍA REGULAR", (0, 200, 200)
        elif score >= 55: return "SIMETRÍA BAJA", (0, 200, 200)
        else: return "SIMETRÍA DEFICIENTE", (0, 0, 200)

    async def start_analysis(self, websocket: WebSocket):
        """Iniciar análisis en tiempo real"""
        self.is_running = True
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            await websocket.send_json({
                "type": "error",
                "message": "No se pudo acceder a la cámara"
            })
            return
        
        logger.info("🔍 Iniciando análisis de simetría facial...")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Voltear frame horizontalmente
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detectar rostros
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                symmetry_score = 0
                
                if len(faces) > 0:
                    face = max(faces, key=lambda f: f[2] * f[3])
                    features = self.detect_facial_features(gray, face)
                    symmetry_score = self.calculate_symmetry_score(features, face[0] + face[2] // 2)
                    frame = self.draw_analysis(frame, face, features, symmetry_score)
                
                # Convertir frame a base64 para enviar al frontend
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Enviar frame y score al frontend
                await websocket.send_json({
                    "type": "video_frame",
                    "frame": f'data:image/jpeg;base64,{frame_base64}',
                    "score": symmetry_score,
                    "interpretation": self.get_interpretation(symmetry_score)[0],
                    "timestamp": cv2.getTickCount() / cv2.getTickFrequency()
                })
                
                # Pequeña pausa para no saturar
                await asyncio.sleep(0.03)  # ~30 FPS
                
        except Exception as e:
            logger.error(f"Error en análisis: {e}")
            await websocket.send_json({
                "type": "error",
                "message": f"Error en el análisis: {str(e)}"
            })
        finally:
            self.stop_analysis()

    def stop_analysis(self):
        """Detener análisis"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info("⏹️ Análisis detenido")

# Instancia global del análisis
facial_analysis = FacialSymmetryAnalysis()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Esperar mensajes del cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "start_analysis":
                logger.info("🎯 Iniciando análisis por solicitud del cliente")
                await facial_analysis.start_analysis(websocket)
                
            elif message.get("action") == "stop_analysis":
                logger.info("⏹️ Deteniendo análisis por solicitud del cliente")
                facial_analysis.stop_analysis()
                await websocket.send_json({
                    "type": "status",
                    "message": "Análisis detenido"
                })
                
    except WebSocketDisconnect:
        logger.info("❌ Cliente desconectado")
        facial_analysis.stop_analysis()
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        facial_analysis.stop_analysis()

@router.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy", 
        "service": "facial_symmetry_analysis",
        "camera_available": facial_analysis.cap is not None and facial_analysis.cap.isOpened() if facial_analysis.cap else False
    })

@router.post("/start")
async def start_analysis():
    """Endpoint HTTP para iniciar análisis (opcional)"""
    return JSONResponse({"message": "Use WebSocket endpoint /facial-symmetry/ws"})

@router.post("/stop")
async def stop_analysis():
    """Endpoint HTTP para detener análisis"""
    facial_analysis.stop_analysis()
    return JSONResponse({"message": "Análisis detenido"})