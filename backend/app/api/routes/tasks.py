from fastapi import APIRouter, HTTPException
from app.core.celery import celery_app

router = APIRouter()

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """
    Obtiene el estado de una tarea asíncrona
    """
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        response = {
            "task_id": task_id,
            "status": task_result.status,
        }
        
        # Si la tarea está lista, incluir resultado
        if task_result.ready():
            response["result"] = task_result.result
        
        return response
        
    except Exception as e:
        raise HTTPException(500, f"Error consultando tarea: {str(e)}")