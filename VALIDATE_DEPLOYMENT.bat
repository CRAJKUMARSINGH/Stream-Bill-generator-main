@echo off
title Deployment Validation

echo ====================================================
echo Stream Bill Generator - Deployment Validation
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running deployment validation...
echo.
python validate_deployment.py

echo.
pause