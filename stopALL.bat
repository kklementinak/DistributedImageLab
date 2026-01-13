@echo off
color 0C
echo ===============================================
echo         STOPPING ALL SERVICES...
echo ===============================================

echo [1/3] Killing Python Worker...
taskkill /F /IM python.exe /T

echo [2/3] Killing .NET WebApp...
taskkill /F /IM dotnet.exe /T
taskkill /F /IM WebApp.exe /T

echo [3/3] Stopping Docker Containers...
cd /d D:\DistributedImageLab\project
docker compose stop

echo.
echo ALL SYSTEMS DOWN.
pause