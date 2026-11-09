@echo off
REM Captura diaria local (mientras el repo no este en GitHub). Programala con el Programador de tareas de Windows.
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (set PY=.venv\Scripts\python.exe) else (set PY=python)
%PY% -m extractores.captura >> calidad\captura_local.log 2>&1
