@echo off
echo ===============================================
echo   CREANDO ENTORNO VIRTUAL PARA EL PROYECTO
echo ===============================================

REM Verificar que Python existe
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python no está instalado o no está en PATH.
    pause
    exit /b
)

echo 🛠️ Creando entorno virtual en /venv...
python -m venv venv

echo 🔌 Activando entorno virtual...
call venv\Scripts\activate

echo 📦 Instalando dependencias del backend...
IF EXIST backend\requirements.txt (
    pip install -r backend\requirements.txt
) ELSE (
    echo ⚠️ No se encontró backend\requirements.txt
)

echo ===============================================
echo   ENTORNO LISTO. FASTAPI YA ESTA INSTALADO.
echo ===============================================
echo Para iniciar el servidor, ejecuta:
echo.
echo   venv\Scripts\activate
echo   uvicorn backend.main:app --reload
echo.
pause
