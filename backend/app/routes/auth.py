from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from backend.database.connection.database import db_manager
from backend.services.auth_service import AuthorizationService
from backend.app.middleware.auth_middleware import crear_token_sesion, eliminar_token_sesion, get_current_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(tags=["autenticacion"])
security = HTTPBearer()

# =============================
#  REGISTRO DE USUARIO
# =============================
@router.post("/register")
async def register(usuario_data: dict):
    """
    Registro de usuario en SQLite.
    """

    tipo = usuario_data.get("document_type")
    numero = usuario_data.get("document_value")
    nombres = usuario_data.get("nombres")
    apellidos = usuario_data.get("apellidos")
    email = usuario_data.get("email")
    fecha_nacimiento = usuario_data.get("fecha_nacimiento")

    if not tipo or not numero:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="document_type y document_value son obligatorios"
        )

    conn = db_manager.get_connection()
    cursor = conn.cursor()

    # Validar si existe
    cursor.execute("SELECT id FROM usuarios WHERE tipo_identificacion=? AND numero_identificacion=?", 
                   (tipo, numero))
    
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este documento ya está registrado"
        )

    cursor.execute("""
        INSERT INTO usuarios 
        (tipo_identificacion, numero_identificacion, nombres, apellidos, email, fecha_nacimiento)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, numero, nombres, apellidos, email, fecha_nacimiento))

    conn.commit()
    conn.close()

    return {"message": "Usuario registrado exitosamente"}


# =============================
#  LOGIN REAL SIN DUI
# =============================
@router.post("/login")
async def login(credenciales: dict):
    """
    Login usando tipo + número de identificación.
    """

    tipo = credenciales.get("document_type")
    numero = credenciales.get("document_value")
    password = credenciales.get("password")

    if not tipo or not numero:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="document_type y document_value son obligatorios"
        )

    # En producción verificarías la contraseña hasheada.
    if password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    conn = db_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombres, apellidos, email, tipo_identificacion, numero_identificacion
        FROM usuarios
        WHERE tipo_identificacion=? AND numero_identificacion=?
    """, (tipo, numero))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    usuario = {
        "id": row[0],
        "nombres": row[1],
        "apellidos": row[2],
        "email": row[3],
        "tipo_identificacion": row[4],
        "numero_identificacion": row[5]
    }

    # Token real
    token = crear_token_sesion(usuario)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario,
        "permisos": {"default": True}
    }


# =============================
#  OBTENER USUARIO
# =============================
@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return current_user


# =============================
#  LOGOUT
# =============================
@router.post("/logout")
async def logout(
    current_user=Depends(get_current_user), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    eliminar_token_sesion(token)
    return {"message": "Sesión cerrada exitosamente"}
