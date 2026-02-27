@echo off
echo ========================================
echo RESTARTING FRONTEND WITH CLEAN CACHE
echo ========================================
echo.

echo Step 1: Removing build cache...
if exist "node_modules\.cache" (
    rmdir /s /q "node_modules\.cache"
    echo ✅ Cache cleared
) else (
    echo ℹ️ No cache found
)

echo.
echo Step 2: Removing build folder...
if exist "build" (
    rmdir /s /q "build"
    echo ✅ Build folder removed
) else (
    echo ℹ️ No build folder found
)

echo.
echo ========================================
echo Cache cleared! Now starting frontend...
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

npm start
