@echo off
setlocal
cd /d "%~dp0"
python a.py
if errorlevel 1 (
    echo.
    echo Could not start Omni Screen Share.
    echo Make sure Python is installed and available as "python".
    pause
)
endlocal
