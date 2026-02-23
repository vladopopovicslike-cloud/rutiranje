@echo off
REM Setup script for Rutiranje project on Windows
REM Installs all required dependencies

echo ==========================================
echo Rutiranje - Python 3 Setup
echo ==========================================
echo.

REM Check if Python 3 is installed
python3 --version >nul 2>&1
if errorlevel 1 (
    echo X Python 3 is not installed
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python3 --version') do set PYTHON_VERSION=%%i
echo Detected: %PYTHON_VERSION%
echo.

REM Upgrade pip
echo Upgrading pip...
python3 -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies from requirements.txt...
python3 -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo X Installation failed
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo You can now run the program with:
echo   python3 main.py
echo.
echo ==========================================
pause
