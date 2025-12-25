@echo off
echo ========================================
echo Starting Frontend Server
echo ========================================
cd /d "%~dp0frontend"
if not exist node_modules (
    echo Installing dependencies...
    call npm.cmd install
)
echo.
echo Starting Vite dev server on http://localhost:5173
echo.
call npm.cmd run dev


