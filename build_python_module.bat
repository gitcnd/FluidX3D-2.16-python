@echo off
REM Build Python extension module for FluidX3D

echo Initializing Visual Studio environment...
call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"

echo.
echo Building Python module...
python setup.py build_ext --inplace

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Build successful!
    echo ============================================
    echo.
    echo You can now test with:
    echo   python -c "import fluidx3d; print(fluidx3d.__version__)"
) else (
    echo.
    echo ============================================
    echo Build failed with error code %ERRORLEVEL%
    echo ============================================
)

pause

