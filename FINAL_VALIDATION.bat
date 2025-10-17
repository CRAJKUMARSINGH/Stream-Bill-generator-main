@echo off
title Final Validation

echo ====================================================
echo Final Validation - Stream Bill Generator
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running final validation...
echo.
python final_validation.py

echo.
pause