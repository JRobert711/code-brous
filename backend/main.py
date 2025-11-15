from fastapi import FastAPI
from app.api.routes.hello import router as hello_router
from app.api.routes.auth import router as auth_router
from app.api.routes.ciudadanos import router as ciudadanos_router
from app.api.routes.drones import router as drones_router

app = FastAPI()

app.include_router(hello_router, prefix="/api", tags=["hello"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(ciudadanos_router, prefix="/api/ciudadanos", tags=["ciudadanos"])
app.include_router(drones_router, prefix="/api/drones", tags=["drones"])

@app.get("/")
def root():
    return {"message": "Backend funcionando correctamente 🚀"}