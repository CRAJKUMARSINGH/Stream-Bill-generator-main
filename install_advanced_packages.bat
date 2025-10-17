@echo off
title Installing Advanced Packages

echo ====================================================
echo Installing Advanced Packages for Enhanced Features
echo ====================================================
echo.

echo Installing advanced Python packages...
pip install -r requirements_advanced.txt
if %errorlevel% neq 0 (
    echo Failed to install advanced packages
    pause
    exit /b %errorlevel%
)

echo.
echo Installing Playwright browsers...
playwright install chromium
if %errorlevel% neq 0 (
    echo Failed to install Playwright browsers
    pause
    exit /b %errorlevel%
)

echo.
echo All advanced packages installed successfully!
echo.
pause