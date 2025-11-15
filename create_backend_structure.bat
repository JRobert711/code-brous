@echo off
echo ===============================================
echo    CREANDO ESTRUCTURA BACKEND - IDN SV
echo ===============================================

REM Crear estructura principal de carpetas
echo Creando estructura de carpetas...

REM Carpeta raíz del proyecto
mkdir backend
cd backend

REM Crear subcarpetas principales
mkdir database
mkdir routes
mkdir services
mkdir models
mkdir config
mkdir utils
mkdir tests
mkdir ai_integrations
mkdir security

REM Crear estructura dentro de database
mkdir database\migrations
mkdir database\seeders

REM Crear estructura dentro de routes
mkdir routes\auth
mkdir routes\ciudadanos
mkdir routes\biometria
mkdir routes\drones
mkdir routes\admin

REM Crear estructura dentro de services
mkdir services\auth
mkdir services\ciudadanos
mkdir services\biometria
mkdir services\drones

REM Crear estructura dentro de models
mkdir models\schemas
mkdir models\database

REM Crear estructura dentro de config
mkdir config\environments

REM Crear estructura dentro de ai_integrations
mkdir ai_integrations\voice
mkdir ai_integrations\face
mkdir ai_integrations\drones

REM Crear estructura dentro de security
mkdir security\encryption
mkdir security\audit

REM Crear archivos __init__.py para hacerlos paquetes Python
echo Creando archivos __init__.py...

REM Archivos __init__.py principales
type nul > __init__.py
type nul > database\__init__.py
type nul > routes\__init__.py
type nul > services\__init__.py
type nul > models\__init__.py
type nul > config\__init__.py
type nul > utils\__init__.py
type nul > tests\__init__.py
type nul > ai_integrations\__init__.py
type nul > security\__init__.py

REM __init__.py en subcarpetas
type nul > database\migrations\__init__.py
type nul > database\seeders\__init__.py

type nul > routes\auth\__init__.py
type nul > routes\ciudadanos\__init__.py
type nul > routes\biometria\__init__.py
type nul > routes\drones\__init__.py
type nul > routes\admin\__init__.py

type nul > services\auth\__init__.py
type nul > services\ciudadanos\__init__.py
type nul > services\biometria\__init__.py
type nul > services\drones\__init__.py

type nul > models\schemas\__init__.py
type nul > models\database\__init__.py

type nul > config\environments\__init__.py

type nul > ai_integrations\voice\__init__.py
type nul > ai_integrations\face\__init__.py
type nul > ai_integrations\drones\__init__.py

type nul > security\encryption\__init__.py
type nul > security\audit\__init__.py

REM Crear archivos Python principales
echo Creando archivos Python principales...

REM Archivo principal
type nul > main.py

REM Archivos de configuración
type nul > config\azure_config.py
type nul > config\database_config.py
type nul > config\security_config.py
type nul > config\environments\development.py
type nul > config\environments\production.py

REM Archivos de base de datos
type nul > database\connection.py
type nul > database\operations.py
type nul > database\migrations\initial_tables.py

REM Archivos de modelos
type nul > models\schemas\ciudadanos.py
type nul > models\schemas\auth.py
type nul > models\schemas\biometria.py
type nul > models\database\ciudadanos_models.py
type nul > models\database\auth_models.py

REM Archivos de rutas
type nul > routes\auth\routes.py
type nul > routes\ciudadanos\routes.py
type nul > routes\biometria\routes.py
type nul > routes\drones\routes.py
type nul > routes\__init__.py

REM Archivos de servicios
type nul > services\auth\auth_service.py
type nul > services\auth\voice_auth_service.py
type nul > services\ciudadanos\ciudadano_service.py
type nul > services\biometria\face_service.py
type nul > services\drones\drone_service.py

REM Archivos de AI integrations
type nul > ai_integrations\voice\voice_processor.py
type nul > ai_integrations\voice\voice_features.py
type nul > ai_integrations\face\face_detection.py
type nul > ai_integrations\face\face_recognition.py
type nul > ai_integrations\drones\drone_ai.py
type nul > ai_integrations\drones\object_detection.py

REM Archivos de seguridad
type nul > security\encryption\aes_encrypt.py
type nul > security\encryption\key_management.py
type nul > security\audit\audit_service.py
type nul > security\audit\access_logs.py

REM Archivos de utilidades
type nul > utils\response_utils.py
type nul > utils\error_handlers.py
type nul > utils\file_utils.py

REM Archivos de tests
type nul > tests\test_auth.py
type nul > tests\test_ciudadanos.py
type nul > tests\test_biometria.py
type nul > tests\conftest.py

REM Crear requirements.txt
echo Creando requirements.txt...
(
echo fastapi==0.104.1
echo uvicorn==0.24.0
echo pyodbc==4.0.39
echo python-multipart==0.0.6
echo python-jose[cryptography]==3.3.0
echo passlib[bcrypt]==1.7.4
echo python-dotenv==1.0.0
echo azure-identity==1.15.0
echo azure-keyvault-secrets==4.7.0
echo azure-storage-blob==12.19.0
echo azure-cognitiveservices-vision-face==0.7.0
echo speechrecognition==3.10.0
echo librosa==0.10.1
echo pydub==0.25.1
echo opencv-python==4.8.1.78
echo numpy==1.24.3
echo pytest==7.4.0
echo pytest-asyncio==0.21.0
) > requirements.txt

REM Crear .env template
echo Creando .env template...
(
echo # Azure Configuration
echo AZURE_SQL_SERVER=your-server.database.windows.net
echo AZURE_SQL_DATABASE=idn-national-db
echo AZURE_SQL_USERNAME=admin-user
echo AZURE_SQL_PASSWORD=your-password
echo.
echo # Azure Storage
echo AZURE_STORAGE_CONNECTION_STRING=your-connection-string
echo.
echo # JWT Configuration
echo JWT_SECRET_KEY=your-super-secret-jwt-key-here
echo JWT_ALGORITHM=HS256
echo JWT_EXPIRE_MINUTES=30
echo.
echo # Face API Configuration
echo AZURE_FACE_API_KEY=your-face-api-key
echo AZURE_FACE_API_ENDPOINT=your-face-api-endpoint
echo.
echo # Voice Auth Configuration
echo VOICE_MATCH_THRESHOLD=0.75
echo.
echo # App Configuration
echo ENVIRONMENT=development
echo CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
) > .env.example

REM Crear archivo README básico
echo Creando README.md...
(
echo # Backend - IDN SV - Identidad Digital Nacional
echo.
echo ## Estructura del Proyecto
echo.
echo ### Carpetas Principales:
echo - `database/`: Conexiones y operaciones de base de datos
echo - `routes/`: Endpoints de la API
echo - `services/`: Lógica de negocio
echo - `models/`: Esquemas y modelos de datos
echo - `ai_integrations/`: Servicios de IA y biometría
echo - `security/`: Encriptación y auditoría
echo - `config/`: Configuraciones de la aplicación
echo.
echo ## Configuración Inicial
echo.
echo 1. Copiar `.env.example` a `.env`
echo 2. Configurar las variables de entorno
echo 3. Instalar dependencias: `pip install -r requirements.txt`
echo 4. Ejecutar: `uvicorn main:app --reload`
echo.
echo ## Endpoints Principales
echo.
echo - `POST /auth/voice-login` - Autenticación por voz
echo - `GET /ciudadanos/{dui}` - Obtener datos de ciudadano
echo - `POST /biometria/face-verify` - Verificación facial
echo - `WS /ws/drones` - WebSocket para drones
) > README.md

echo ===============================================
echo    ESTRUCTURA CREADA EXITOSAMENTE!
echo ===============================================
echo.
echo Carpetas creadas:
echo ✅ backend/
echo ✅ database/ con migrations/ y seeders/
echo ✅ routes/ con auth/, ciudadanos/, biometria/, drones/
echo ✅ services/ con módulos especializados
echo ✅ ai_integrations/ con voice/, face/, drones/
echo ✅ security/ con encryption/ y audit/
echo ✅ Archivos de configuración y modelos
echo.
echo Próximos pasos:
echo 1. Copia .env.example a .env y configura tus variables
echo 2. Instala las dependencias adicionales: pip install -r requirements.txt
echo 3. Ejecuta: uvicorn main:app --reload
echo.
echo ¡Listo para desarrollar! 🚀
pause