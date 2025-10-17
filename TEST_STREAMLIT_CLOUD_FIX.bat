@echo off
title Streamlit Cloud Deployment Fix Test

echo ====================================================
echo Streamlit Cloud Deployment Fix Test
echo ====================================================
echo This script tests the fixes for Streamlit Cloud deployment issues.
echo.

echo Changing to project directory...
cd /d "c:\Users\Rajkumar\Stream-Bill-generator-main"

echo.
echo Testing Python imports...
python test_streamlit_imports.py
if %errorlevel% neq 0 (
    echo ❌ Import test failed!
    pause
    exit /b %errorlevel%
)

echo.
echo Starting Streamlit app...
echo If the app starts successfully, the import fixes are working.
echo Close the Streamlit window to continue...
echo.
streamlit run app/main.py

echo.
echo Test completed successfully!
pause