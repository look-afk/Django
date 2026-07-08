@echo off
set "ROOT=%~dp0.."
"%ROOT%\venv\Scripts\python.exe" "%ROOT%\manage.py" makemigrations %*
