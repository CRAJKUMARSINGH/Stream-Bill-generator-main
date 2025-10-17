@echo off
title Testing Modular Fixes

echo ====================================================
echo Testing Modular Fixes
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running modular fixes test...
echo.
python test_modular_fixes.py

echo.
pause