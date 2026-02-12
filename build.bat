@echo off
echo ========================================
echo Mouse Jiggler Build Script
echo ========================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [2/4] Creating icon file...
python create_icon.py
if errorlevel 1 (
    echo Failed to create icon!
    pause
    exit /b 1
)
echo.

echo [3/4] Building executable...
pyinstaller --onefile --windowed --icon=coffee_cup.ico --name=MouseJiggler mouse_jiggler.py
if errorlevel 1 (
    echo Failed to build executable!
    pause
    exit /b 1
)
echo.

echo [4/4] Cleaning up...
if exist build rmdir /s /q build
if exist MouseJiggler.spec del MouseJiggler.spec
echo.

echo ========================================
echo Build complete!
echo.
echo Your executable is at: dist\MouseJiggler.exe
echo ========================================
pause
