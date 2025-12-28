@echo off
:: Ensure we are running in the script's directory
cd /d "%~dp0"

echo.
echo ===================================================
echo   Scientific Calculator - Windows Build Script
echo ===================================================
echo.

:: 1. Check if Python is installed/in PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was NOT found!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: When installing, make sure to check the box:
    echo "Add Python to environment variables" or "Add Python to PATH"
    echo.
    pause
    exit /b
)

:: 2. Check if pip is working
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 'pip' command not found, but Python is installed.
    echo This usually means the Scripts folder is not in your PATH.
    echo.
    echo Try running this script again after reinstalling Python with "Add to PATH" checked.
    echo.
    pause
    exit /b
)

echo [OK] Python found. Installing required packages...
:: Use --no-cache-dir to prevent file access errors on Windows
python -m pip install --upgrade pip --user --no-cache-dir
python -m pip install numpy matplotlib pyinstaller --user --no-cache-dir

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install packages. 
    echo Please try running this script as Administrator or check your internet connection.
    echo.
    pause
    exit /b
)

echo.
echo [OK] Dependencies installed. Building application...
:: Use "python -m PyInstaller" to ensure we find the command even if PATH isn't perfect
python -m PyInstaller --noconfirm --onefile --windowed --name "ScientificCalculator" --icon "Calculator.ico" --distpath "%USERPROFILE%\Desktop" gui_calculator_graphing.py

echo.
if exist "%USERPROFILE%\Desktop\ScientificCalculator.exe" (
    echo ===================================================
    echo   BUILD SUCCESSFUL!
    echo ===================================================
    echo.
    echo Your application is ready on your Desktop:
    echo %USERPROFILE%\Desktop\ScientificCalculator.exe
    echo.
) else (
    echo [ERROR] Build failed. Please check the error messages above.
)
pause
