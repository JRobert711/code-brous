@echo off
echo ===============================================
echo      CREANDO BACKEND FASTAPI LIMPIO
echo ===============================================

REM Crear carpeta backend
mkdir backend
cd backend

REM Crear estructura mínima
mkdir app
mkdir app\api
mkdir app\api\routes
mkdir app\db
mkdir app\models
mkdir app\core

REM Crear __init__ para paquetes
type nul > app\__init__.py
type nul > app\api\__init__.py
type nul > app\api\routes\__init__.py
type nul > app\db\__init__.py
type nul > app\models\__init__.py
type nul > app\core\__init__.py

REM Archivos mínimos
type nul > main.py
type nul > app\api\routes\hello.py
type nul > app\core\config.py
type nul > requirements.txt

echo fastapi==0.104.1>requirements.txt
echo uvicorn==0.24.0>>requirements.txt

echo ===============================================
echo    ESTRUCTURA CREADA
echo    Ahora ejecuta: setup_env.bat
echo ===============================================
pause
