@echo off
cd /d %~dp0

echo ✅ Compilando LTerminal...

pyinstaller --onefile --console --icon=terminal.ico ^
--hidden-import=textual ^
--add-data "LTerminal\\resources\\styles.css;LTerminal\\resources" ^
--add-data "LTerminal\\config.json;LTerminal" ^
start.py

echo.
echo ✅ Compilación completada. Ejecutable en: dist\start.exe
pause
