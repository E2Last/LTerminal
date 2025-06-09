@echo off
cd /d %~dp0

echo ✅ Compilando LTerminal...

:: Ruta al PyInstaller instalado por pip
set PYINSTALLER_EXE=%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe

:: Verifica si existe PyInstaller
if not exist "%PYINSTALLER_EXE%" (
    echo ❌ No se encontró PyInstaller en la ruta esperada:
    echo    %PYINSTALLER_EXE%
    echo Por favor, revisa si Python está correctamente instalado.
    pause
    exit /b
)

:: Ejecuta la compilación
"%PYINSTALLER_EXE%" --onefile --console --icon=terminal.ico ^
--name ETerminal ^
--hidden-import=textual ^
--add-data "LTerminal\\resources\\styles.css;LTerminal\\resources" ^
--add-data "LTerminal\\config.json;LTerminal" ^
start.py

echo.
echo ✅ Compilación completada. Ejecutable en: dist\start.exe
pause
