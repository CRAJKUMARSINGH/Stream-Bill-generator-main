@echo off
title Testing App Launch

echo ====================================================
echo Testing App Launch Readiness
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Testing app launch readiness...
echo.
python test_launch.py

echo.
pause