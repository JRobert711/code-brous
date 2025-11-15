from fastapi import FastAPI
from backend.routes.auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def health():
    return {"status": "OK"}
