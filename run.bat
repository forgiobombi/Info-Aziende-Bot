@echo off
REM Info Aziende Bot - Startup Script for Windows

echo Starting Info Aziende Bot...
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure your tokens.
    echo.
    echo Run: copy .env.example .env
    echo Then edit .env with your Discord and OpenAPI tokens.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import discord" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the bot
echo Starting bot...
python bot.py

pause
