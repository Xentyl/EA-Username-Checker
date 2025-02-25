@echo off
REM Ensure Python is installed and in the PATH
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in the PATH.
    pause
    exit /b 1
)

REM Run the Python script
python checker.py

REM Pause to see the output
pause