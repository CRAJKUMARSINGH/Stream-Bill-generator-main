@echo off
title Performance Monitoring Dashboard

echo ====================================================
echo Performance Monitoring Dashboard
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Checking required packages...
python -c "import streamlit, pandas, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Required packages not found. Please run install_advanced_packages.bat first.
    pause
    exit /b 1
)

echo Starting monitoring dashboard...
echo.
echo The dashboard will be available at: http://localhost:8502
echo.
echo Close this window to stop the server
echo.

python -m streamlit run scripts/monitoring_dashboard.py --server.port 8502

pause