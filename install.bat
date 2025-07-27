@echo off
echo ==============================================
echo Balloon Pop Game - Setup Script for Windows
echo ==============================================

REM Check if Python 3.10 is installed
echo [CHECK] Detecting Python 3.10...
py -3.10 --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python 3.10 is not installed or not added to PATH.
    echo Please install Python 3.10 and ensure it's added to your system PATH.
    pause
    exit /b
)

echo [INFO] Python 3.10 detected.
echo.

REM Upgrade pip
echo [STEP 1] Upgrading pip...
py -3.10 -m pip install --upgrade pip
echo.

REM Install requirements
echo [STEP 2] Installing required Python libraries...
py -3.10 -m pip install -r requirements.txt
echo.

REM Done
echo [✅ SUCCESS] All dependencies are installed!
echo.
echo [🎮 TO PLAY] Use the command:
echo     py -3.10 BalloonPop.py
echo.
pause
