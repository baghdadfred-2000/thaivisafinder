@echo off
REM Double-click this to launch a local preview of the site (clean URLs, footer, assets).
REM It starts a small PowerShell web server from this folder and opens your browser.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0preview.ps1"
pause
