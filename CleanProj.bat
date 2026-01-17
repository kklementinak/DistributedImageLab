@echo off
color 0E
echo ===============================================
echo   CLEANING PROJECT (Removing temporary files)
echo ===============================================

echo.
echo [1/3] Deleting Python Virtual Environment (venv)...
if exist "project\Worker\venv" (
    rmdir /s /q "project\Worker\venv"
    echo    - venv deleted.
) else (
    echo    - venv not found ^(already clean^).
)

echo.
echo [2/3] Deleting Python Cache...
if exist "project\Worker\__pycache__" (
    rmdir /s /q "project\Worker\__pycache__"
)
if exist "project\Worker\*.spec" del "project\Worker\*.spec"

echo.
echo [3/3] Deleting .NET Build Artifacts (bin, obj)...
if exist "project\WebApp\bin" (
    rmdir /s /q "project\WebApp\bin"
    echo    - bin deleted.
)
if exist "project\WebApp\obj" (
    rmdir /s /q "project\WebApp\obj"
    echo    - obj deleted.
)

echo.
echo ===============================================
echo PROJECT IS CLEAN! (Ready to zip/upload)
echo ===============================================
pause