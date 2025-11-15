# Backend - IDN SV - Identidad Digital Nacional

## Estructura del Proyecto

### Carpetas Principales:
- `database/`: Conexiones y operaciones de base de datos
- `routes/`: Endpoints de la API
- `services/`: Lógica de negocio
- `models/`: Esquemas y modelos de datos
- `ai_integrations/`: Servicios de IA y biometría
- `security/`: Encriptación y auditoría
- `config/`: Configuraciones de la aplicación

## Configuración Inicial

1. Copiar `.env.example` a `.env`
2. Configurar las variables de entorno
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `uvicorn main:app --reload`

## Endpoints Principales

- `POST /auth/voice-login` - Autenticación por voz
- `GET /ciudadanos/{dui}` - Obtener datos de ciudadano
- `POST /biometria/face-verify` - Verificación facial
- `WS /ws/drones` - WebSocket para drones
