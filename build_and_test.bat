@echo off
REM Build and test script for FluidX3D Python module

echo ======================================
echo Building FluidX3D Python Module
echo ======================================

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info

echo.
echo Building package...
python -m build

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ======================================
echo Build successful!
echo ======================================
echo.
echo Files created in dist/:
dir /b dist\
echo.
echo To upload to Test PyPI:
echo   python -m twine upload --repository testpypi dist/*
echo.
echo To upload to PyPI:
echo   python -m twine upload dist/*
echo.
pause

