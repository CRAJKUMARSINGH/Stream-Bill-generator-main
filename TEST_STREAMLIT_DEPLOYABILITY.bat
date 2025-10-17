@echo off
title Streamlit App Deployability Test

echo ====================================================
echo Streamlit App Deployability Test
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running comprehensive deployability test...
echo.
python streamlit_deployability_test.py

echo.
pause