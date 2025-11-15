from celery import Celery
from app.core.config import settings
import os

# Si estamos en desarrollo sin Redis, usar modo eager
if os.getenv("USE_FAKE_REDIS", "false").lower() == "true":
    celery_app = Celery("code_brous")
    celery_app.conf.update(
        task_always_eager=True,  # Ejecuta tareas sincrónicamente
        task_eager_propagates=True,
    )
    print("🔧 Celery en modo desarrollo (sin Redis requerido)")
else:
    celery_app = Celery(
        "code_brous",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "app.tasks.audio_tasks",
            "app.tasks.image_tasks"
        ]
    )
    
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="America/Santo_Domingo",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=300,
        worker_prefetch_multiplier=1,
        task_acks_late=True,
    )