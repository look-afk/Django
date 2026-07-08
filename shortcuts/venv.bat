@echo off
set "ROOT=%~dp0.."
set "VENV_DIR=%ROOT%\venv"

if exist "%VENV_DIR%" (
    echo Virtual environment already exists at %VENV_DIR%
) else (
    py -3 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed and available as py.
    ) else (
        echo Virtual environment created at %VENV_DIR%
    )
)
