@echo off
title Testing All Batch Files

echo ====================================================
echo Testing All Batch Files
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo Running batch files test...
echo.
python test_all_batch_files.py

echo.
pause