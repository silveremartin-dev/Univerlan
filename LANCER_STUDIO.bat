@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo   Univerlan Studio - Langue Interstellaire Auxiliaire
echo ========================================================
echo Demarrage du serveur local et ouverture du navigateur...
echo.

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py scripts\run_studio.py
    goto end
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python scripts\run_studio.py
    goto end
)

if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" scripts\run_studio.py
    goto end
)

echo Python n'a pas ete detecte dans l'environnement.
echo Ouverture directe du studio dans votre navigateur par defaut...
start "" "%~dp0index.html"

:end
pause
