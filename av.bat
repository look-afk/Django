@echo off
set "ROOT=%~dp0"
set "VENV_ACTIVATE=%ROOT%venv\Scripts\activate.bat"

if exist "%VENV_ACTIVATE%" (
    call "%VENV_ACTIVATE%"
) else (
    echo Virtual environment not found at %ROOT%venv. Creating it now...
    call "%ROOT%venv.bat"
    if exist "%VENV_ACTIVATE%" (
        call "%VENV_ACTIVATE%"
    ) else (
        echo Failed to activate the virtual environment.
    )
)
