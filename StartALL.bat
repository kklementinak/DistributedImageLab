@echo off
color 0A
echo ===============================================
echo     STARTING DISTRIBUTED IMAGE LAB SYSTEM
echo ===============================================

:: 1. Стартиране на Redis
echo [*] Starting Redis...
start "1. Infrastructure (Redis)" cmd /k "cd /d D:\DistributedImageLab\project && docker compose up"

:: Изчакваме 5 секунди
timeout /t 5 /nobreak >nul

:: 2. Стартиране на Уеб Сайта
echo [*] Starting WebApp...
start "2. Web App (.NET)" cmd /k "cd /d D:\DistributedImageLab\project\WebApp && dotnet run"

:: 3. Стартиране на Работника (с инсталиране на библиотеки)
echo [*] Starting Python Worker...
echo     Checking dependencies from requirements.txt...
start "3. Python Worker" cmd /k "cd /d D:\DistributedImageLab\project\Worker && venv\Scripts\activate && pip install -r requirements.txt && python worker.py"

echo.
echo ALL SYSTEMS LAUNCHED!
echo You can minimize this window, but don't close the others.
echo.
pause