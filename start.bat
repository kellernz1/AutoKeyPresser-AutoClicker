@echo off
cd /d "%~dp0"
pyw tecla_automatica.py
if errorlevel 1 py tecla_automatica.py
