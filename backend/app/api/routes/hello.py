from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"status": "ok", "message": "Hola Mauricio, FastAPI está vivo."}
