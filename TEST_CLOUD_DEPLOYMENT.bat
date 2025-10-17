@echo off
title Testing Cloud Deployment Configuration

echo ====================================================
echo Testing Cloud Deployment Configuration
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Checking basic requirements...
python -c "import streamlit, pandas, pdfkit, docx, num2words, jinja2, pypdf, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Some basic packages not found. Make sure you have installed requirements_basic.txt
    echo    This is normal for cloud deployment testing.
    echo.
)

echo Running cloud deployment test...
echo.
python test_cloud_deployment.py

echo.
pause