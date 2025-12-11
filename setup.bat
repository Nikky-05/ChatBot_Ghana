@echo off
echo ========================================
echo CatBot Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo [3/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [4/4] Parsing FAQs...
python parse_faqs.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to parse FAQs
    pause
    exit /b 1
)
echo ✓ FAQs parsed successfully

echo.
echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo To run the application:
echo   1. Activate venv: venv\Scripts\activate
echo   2. Run app: python app.py
echo   3. Visit: http://localhost:5000
echo.
pause
