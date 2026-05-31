@echo off
chcp 65001 >nul
echo ============================================================
echo   Aws Eal Saffar Project - Automatic Setup for Windows
echo   مشروع عوس آل الصفّار - الإعداد التلقائي للويندوز
echo ============================================================
echo.

REM Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Create virtual environment
if not exist venv (
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/4] Virtual environment already exists
)
echo.

REM Activate venv
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip and install requirements
echo [4/4] Installing dependencies (this may take a few minutes)...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

echo ============================================================
echo   Setup complete! - تم الإعداد بنجاح
echo ============================================================
echo.
echo To run the project / لتشغيل المشروع:
echo   1. venv\Scripts\activate
echo   2. python -m src.main
echo.
pause
