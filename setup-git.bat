@echo off
REM ============================================================
REM  ThaiVisaFinder - Git setup and push to GitHub
REM  Double-click this file, or run it from this folder.
REM ============================================================
cd /d "%~dp0"

echo.
echo === Initializing git repository ===
git init
if errorlevel 1 goto :error

echo.
echo === Setting branch to main ===
git branch -M main

echo.
echo === Adding all files ===
git add .

echo.
echo === Creating initial commit ===
git commit -m "Initial commit: ThaiVisaFinder static site, assets, and SEO files"

echo.
echo === Configuring remote 'origin' ===
git remote remove origin 2>nul
git remote add origin https://github.com/baghdadfred-2000/thaivisafinder.git

echo.
echo === Pushing to GitHub ===
git push -u origin main
if errorlevel 1 goto :error

echo.
echo === Verifying: git remote -v ===
git remote -v

echo.
echo === Verifying: git status ===
git status

echo.
echo === DONE ===
pause
exit /b 0

:error
echo.
echo *** Something failed. Read the message above. ***
echo If push failed, you may need to sign in to GitHub when prompted.
pause
exit /b 1
