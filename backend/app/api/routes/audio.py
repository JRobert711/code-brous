from fastapi import APIRouter, UploadFile, File, HTTPException
from app.tasks.audio_tasks import process_audio_task
from app.core.redis import redis_client
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/process-audio")
async def process_audio(audio_file: UploadFile = File(...)):
    """
    Endpoint para procesar audio de forma asíncrona
    """
    try:
        # Validar tipo de archivo
        if not audio_file.filename.endswith(('.wav', '.mp3', '.m4a')):
            raise HTTPException(400, "Formato de audio no soportado")
        
        # Leer archivo
        audio_data = await audio_file.read()
        
        # Ejecutar tarea asíncrona
        task = process_audio_task.delay(audio_data, audio_file.filename)
        
        # Guardar en Redis para seguimiento
        redis_client.setex(
            f"audio_task:{task.id}",
            3600,  # Expira en 1 hora
            "processing"
        )
        
        return {
            "message": "Audio en procesamiento",
            "task_id": task.id,
            "status_url": f"/api/v1/tasks/{task.id}/status"
        }
        
    except Exception as e:
        logger.error(f"Error en process-audio: {str(e)}")
        raise HTTPException(500, f"Error interno: {str(e)}")