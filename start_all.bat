@echo off
echo ============================================
echo   Dashboard Service - Full Start
echo ============================================
echo.
echo Starting Backend and Frontend...
echo.

REM Запуск backend в новом окне
start "Dashboard Backend" cmd /k "cd backend && if not exist venv (python -m venv venv) && call venv\Scripts\activate.bat && pip install -r requirements.txt >nul 2>&1 && echo Backend started on http://localhost:8000 && python run.py"

REM Ждем 5 секунд, чтобы backend запустился
timeout /t 5 /nobreak >nul

REM Запуск frontend в новом окне
start "Dashboard Frontend" cmd /k "cd frontend && if not exist node_modules (npm install) && echo Frontend started on http://localhost:5173 && npm run dev"

echo.
echo ============================================
echo   Both services are starting...
echo ============================================
echo.
echo Backend:  http://localhost:8000/api/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to open Frontend in browser...
pause >nul

start http://localhost:5173

echo.
echo Services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause









