from fastapi import FastAPI
from backend.app.api.routes.hello import router as hello_router

app = FastAPI()

app.include_router(hello_router, prefix="/api", tags=["hello"])

@app.get("/")
def root():
    return {"message": "Backend funcionando correctamente 🚀"}
