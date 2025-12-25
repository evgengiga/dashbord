@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting FastAPI server on http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo.
python run.py


