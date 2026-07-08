@echo off
set "ROOT=%~dp0.."
call "%ROOT%\venv\Scripts\activate.bat"
"%ROOT%\venv\Scripts\python.exe" "%ROOT%\manage.py" migrate %*
