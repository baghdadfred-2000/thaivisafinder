# ThaiVisaFinder - Git setup and push to GitHub (PowerShell)
# Run from the project folder, or just run this script.
Set-Location -Path $PSScriptRoot

git init
git branch -M main
git add .
git commit -m "Initial commit: ThaiVisaFinder static site, assets, and SEO files"
git remote remove origin 2>$null
git remote add origin https://github.com/baghdadfred-2000/thaivisafinder.git
git push -u origin main

Write-Host "`n=== git remote -v ===" -ForegroundColor Cyan
git remote -v
Write-Host "`n=== git status ===" -ForegroundColor Cyan
git status
