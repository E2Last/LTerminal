@echo off
cd /d "C:\Users\Archivos\LTerminal"
echo ✅ Directorio de trabajo: %CD%

echo ✅ Compilando LTerminal...

:: Mostrar información de Python para depuración
echo 🔍 Verificando Python...
python --version
where python
echo.

:: Verificar si pyinstaller está en el PATH
echo 🔍 Buscando PyInstaller...
where pyinstaller >nul 2>&1
if %errorlevel%==0 (
    set "PYINSTALLER_EXE=pyinstaller"
    echo ✅ PyInstaller encontrado en