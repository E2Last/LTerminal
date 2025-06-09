@echo off
cd /d %~dp0

echo ✅ Compilando LTerminal...

:: Verificar si pyinstaller está en el PATH
where pyinstaller >nul 2>&1
if %errorlevel%==0 (
    set "PYINSTALLER_EXE=pyinstaller"
) else (
    :: Ruta alternativa si no está en PATH (para Python 3.11 instalado desde Microsoft Store)
    set "PYINSTALLER_EXE=%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe"
    
    if not exist "%PYINSTALLER_EXE%" (
        echo ❌ No se encontró PyInstaller en el PATH ni en la ruta local esperada.
        pause
        exit /b
    )
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
