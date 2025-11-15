# backend/services/recaptcha_service.py
import requests
import os
from fastapi import HTTPException, status
from typing import Optional

class RecaptchaService:
    def __init__(self):
        # Tu clave secreta de reCAPTCHA
        self.secret_key = "6LfitQ0sAAAAAEkZzkU0isAqWo8X-W1cMsWljS-2"
        self.verify_url = "https://www.google.com/recaptcha/api/siteverify"
    
    async def verify_recaptcha(self, token: Optional[str]) -> bool:
        """
        Verificar token de reCAPTCHA con Google
        """
        # Si no hay token en desarrollo, permitir continuar
        if not token and os.getenv("ENVIRONMENT") == "development":
            print("🔧 Modo desarrollo: reCAPTCHA omitido")
            return True
            
        # En desarrollo, aceptar tokens de prueba
        if os.getenv("ENVIRONMENT") == "development" and token in ["test_token", "development_token"]:
            print("🔧 Modo desarrollo: token de prueba aceptado")
            return True
        
        if not token:
            print("❌ Token reCAPTCHA faltante")
            return False
            
        try:
            response = requests.post(
                self.verify_url,
                data={
                    "secret": self.secret_key,
                    "response": token
                },
                timeout=10
            )
            
            result = response.json()
            
            # Debug
            print(f"🔍 reCAPTCHA Response: {result}")
            
            # Verificar éxito y score (para v3)
            success = result.get("success", False)
            score = result.get("score", 0.0)
            
            # Para reCAPTCHA v2, success es suficiente
            # Para v3, podrías verificar el score también
            if success:
                print(f"✅ reCAPTCHA verificado exitosamente (score: {score})")
                return True
            else:
                print(f"❌ reCAPTCHA falló: {result.get('error-codes', ['Unknown error'])}")
                return False
            
        except Exception as e:
            print(f"❌ Error verificando reCAPTCHA: {e}")
            # En desarrollo, permitir continuar
            if os.getenv("ENVIRONMENT") == "development":
                print("🔧 Modo desarrollo: error de reCAPTCHA omitido")
                return True
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error en verificación de seguridad"
            )

recaptcha_service = RecaptchaService()