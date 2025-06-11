@echo off
cd /d %~dp0

echo ✅ Compilando ETerminal...

call venv\Scripts\activate.bat

rmdir /s /q build
rmdir /s /q dist
del ETerminal.spec

pyinstaller ^
--noconfirm ^
--clean ^
--icon=terminal.ico ^
--name=ETerminal ^
--collect-submodules LTerminal.utils ^
--add-data "LTerminal\\resources\\styles.css;LTerminal/resources" ^
--add-data "LTerminal\\config.json;LTerminal" ^
start.py

echo ✅ Ejecutable generado: dist\ETerminal\ETerminal.exe
pause
