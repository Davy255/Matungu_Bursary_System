@echo off
echo ============================================================
echo    OPENING ALL SVG DIAGRAMS IN BROWSER
echo ============================================================
echo.
echo Instructions to convert SVG to PNG:
echo.
echo 1. Wait for all diagrams to open in browser tabs
echo 2. For each tab, press: Win + Shift + S
echo 3. Select the diagram area with your mouse
echo 4. Open Paint (Win + R, type "mspaint")
echo 5. Paste (Ctrl + V)
echo 6. File - Save As - PNG
echo.
echo ============================================================
pause

start "" "01-system-architecture-3d.svg"
timeout /t 2 /nobreak >nul

start "" "02-application-flow-3d.svg"
timeout /t 2 /nobreak >nul

start "" "03-erd-3d.svg"
timeout /t 2 /nobreak >nul

start "" "04-database-detailed-3d.svg"
timeout /t 2 /nobreak >nul

start "" "05-system-modules-3d.svg"
timeout /t 2 /nobreak >nul

echo.
echo All diagrams opened! Use Win+Shift+S to screenshot each one.
echo.
pause
