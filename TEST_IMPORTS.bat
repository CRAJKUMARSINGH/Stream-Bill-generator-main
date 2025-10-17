@echo off
title Testing Module Imports

echo ====================================================
echo Testing Module Imports
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running import tests...
echo.
python test_imports.py

echo.
pause