from fastapi import APIRouter, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel
import requests
import os

# ------------------------------------------------------------------
# Configuración del CAPTCHA (pon tu SECRET KEY real)
# ------------------------------------------------------------------
RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET", "TU_SECRET_KEY_AQUI")

router = APIRouter(tags=["Autenticación"])

# ------------------------------------------------------------------
# Esquema de entrada del login
# ------------------------------------------------------------------
class LoginRequest(BaseModel):
    dui: str
    password: str
    captcha_token: str


# ------------------------------------------------------------------
# Función para verificar el reCAPTCHA
# ------------------------------------------------------------------
def verificar_captcha(token: str) -> bool:
    """Valida el token del captcha con Google"""
    url = "https://www.google.com/recaptcha/api/siteverify"

    data = {
        "secret": RECAPTCHA_SECRET,
        "response": token
    }

    response = requests.post(url, data=data)
    resultado = response.json()

    # El campo importante es "success"
    return resultado.get("success", False)


# ------------------------------------------------------------------
# Aquí debes conectar tu lógica de usuario
# (BD, ORM, verificación de contraseña, etc.)
# ------------------------------------------------------------------
def autenticar_usuario(dui: str, password: str):
    """
    Simulación temporal:
    Reemplaza esto con tu consulta real a base de datos.
    """
    if dui == "00000000-0" and password == "password123":
        return {
            "id": 1,
            "dui": "00000000-0",
            "nombres": "Usuario",
            "apellidos": "de Prueba",
            "email": "test@email.com",
            "sector": "ciudadano",
            "nivel_acceso": 1
        }

    return None


# ------------------------------------------------------------------
# Generador de token (JWT)
# Sustituye esto si tu proyecto ya tiene uno
# ------------------------------------------------------------------
def generar_token(usuario: dict) -> str:
    """
    Token de ejemplo.
    Reemplázalo con tu JWT real.
    """
    return f"token_simulado_{usuario['id']}"


# ------------------------------------------------------------------
# RUTA principal: LOGIN
# ------------------------------------------------------------------
@router.post("/login")
def login(payload: LoginRequest = Body(...)):
    
    # -----------------------------
    # 1. Validación de CAPTCHA
    # -----------------------------
    if not payload.captcha_token:
        raise HTTPException(status_code=400, detail="Captcha no enviado.")

    if not verificar_captcha(payload.captcha_token):
        raise HTTPException(status_code=400, detail="Captcha inválido. Intenta de nuevo.")

    # -----------------------------
    # 2. Autenticación del usuario
    # -----------------------------
    usuario = autenticar_usuario(payload.dui, payload.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

    # -----------------------------
    # 3. Generación de token
    # -----------------------------
    token = generar_token(usuario)

    # -----------------------------
    # 4. Respuesta estándar
    # -----------------------------
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario
    }
