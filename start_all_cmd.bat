@echo off
echo ============================================
echo   Dashboard Service - Full Start (CMD)
echo ============================================
echo.
echo Starting Backend and Frontend...
echo.

REM Запуск backend в новом окне CMD
start "Dashboard Backend" cmd /k "cd /d %~dp0backend && (if not exist venv python -m venv venv) && call venv\Scripts\activate.bat && pip install -q -r requirements.txt && echo Backend started on http://localhost:8000 && python run.py"

REM Ждем 5 секунд
timeout /t 5 /nobreak >nul

REM Запуск frontend в новом окне CMD
start "Dashboard Frontend" cmd /k "cd /d %~dp0frontend && (if not exist node_modules call npm install) && echo Frontend started on http://localhost:5173 && call npm run dev"

echo.
echo ============================================
echo   Both services are starting...
echo ============================================
echo.
echo Backend:  http://localhost:8000/api/docs
echo Frontend: http://localhost:5173
echo.
echo Waiting for services to start...
timeout /t 15 /nobreak >nul

echo Opening browser...
start http://localhost:5173

echo.
echo Services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause



