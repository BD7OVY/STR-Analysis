@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
cd tools
set "PY=%USERPROFILE%\.workbuddy\binaries\python\versions\3.13.12\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" generate_dashboard.py
echo Generating dashboard ...
echo Starting local server on port 8080 ...
start "" "%PY%" server.py
timeout /t 2 >nul
start "" "http://localhost:8080"
