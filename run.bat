@echo off
chcp 65001 >nul
echo Launching project... / جاري تشغيل المشروع...
echo.

if not exist venv (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first / يرجى تشغيل setup.bat أولاً
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python -m src.main

pause
