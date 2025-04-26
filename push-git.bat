@echo off
cd /d C:\Users\Home\git\runpod-vs\

:: Get commit message from popup
for /f "usebackq delims=" %%i in (`powershell -command ^
  "$commit=Read-Host 'Enter Commit Message'; if ($commit -eq '') {exit 1} else {Write-Output $commit}"`) do set "commitMessage=%%i"

:: Exit if no message entered
if "%commitMessage%"=="" (
    echo No commit message entered. Exiting.
    press any key to continue...
    pause >nul
    exit /b
)

git add .
git commit -m "%commitMessage%"
git push

echo.
echo ✅ Commit and push successful: %commitMessage%
echo Press any key to close...
pause >nul
