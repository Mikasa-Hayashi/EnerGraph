@echo off
chcp 65001
setlocal enabledelayedexpansion

:: === Set defaults
if not defined PYTHON (set "PYTHON=python")
if not defined VENV_DIR (set "VENV_DIR=%~dp0venv")

:: === Create tmp directory for logs
set LOG_DIR=tmp
set STDOUT_FILE=%LOG_DIR%\stdout.txt
set STDERR_FILE=%LOG_DIR%\stderr.txt
mkdir %LOG_DIR% 2>nul

:: === Check if Python works
%PYTHON% -c "" >%STDOUT_FILE% 2>%STDERR_FILE%
if %ERRORLEVEL% NEQ 0 (
    echo Python launch failed.
    goto show_errors
)

:: === Check pip
%PYTHON% -m pip --version >%STDOUT_FILE% 2>%STDERR_FILE%
if %ERRORLEVEL% NEQ 0 (
    echo pip not found. Trying to install...
    if not defined PIP_INSTALLER_LOCATION (
        goto show_errors
    )
    %PYTHON% "%PIP_INSTALLER_LOCATION%" >%STDOUT_FILE% 2>%STDERR_FILE%
    if %ERRORLEVEL% NEQ 0 (
        echo pip installation failed.
        goto show_errors
    )
)

:: === Create virtual environment if not exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON% -m venv "%VENV_DIR%" >%STDOUT_FILE% 2>%STDERR_FILE%
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        goto show_errors
    )
)

:: === Activate venv
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

:: === Upgrade pip and install requirements
echo Installing dependencies...
pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
)

:: === Launch main.py
echo Launching EnerGraph...
python main.py
exit /b

:: === Error display block
:show_errors
echo.
echo Error occurred. Exit code: %ERRORLEVEL%
echo -------------------- stdout --------------------
type %STDOUT_FILE%
echo -------------------- stderr --------------------
type %STDERR_FILE%
pause
exit /b
