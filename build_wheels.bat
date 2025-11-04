@echo off
REM Build binary wheels for all Python versions
REM Users will install pre-compiled wheels - no compilation needed!

echo ======================================
echo Building FluidX3D Binary Wheels
echo ======================================
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info

echo Cleaned previous builds
echo.

REM Find all installed Python versions and build wheels
REM Note: You need to have each Python version installed!

echo Checking for Python installations...
echo.

REM Try Python 3.11
py -3.11 --version 2>nul
if %errorlevel% == 0 (
    echo Building wheel for Python 3.11...
    py -3.11 -m pip install --upgrade build wheel
    py -3.11 -m build --wheel
    echo.
) else (
    echo Python 3.11 not found, skipping...
)

REM Try Python 3.12
py -3.12 --version 2>nul
if %errorlevel% == 0 (
    echo Building wheel for Python 3.12...
    py -3.12 -m pip install --upgrade build wheel
    py -3.12 -m build --wheel
    echo.
) else (
    echo Python 3.12 not found, skipping...
)

REM Try Python 3.13
py -3.13 --version 2>nul
if %errorlevel% == 0 (
    echo Building wheel for Python 3.13...
    py -3.13 -m pip install --upgrade build wheel
    py -3.13 -m build --wheel
    echo.
) else (
    echo Python 3.13 not found, skipping...
)

REM Try Python 3.14
py -3.14 --version 2>nul
if %errorlevel% == 0 (
    echo Building wheel for Python 3.14...
    py -3.14 -m pip install --upgrade build wheel
    py -3.14 -m build --wheel
    echo.
) else (
    echo Python 3.14 not found, skipping...
)

echo.
echo ======================================
echo Build Complete!
echo ======================================
echo.
echo Binary wheels created in dist/:
dir /b dist\*.whl
echo.
echo These are PRE-COMPILED and ready to install!
echo Users do NOT need Visual Studio!
echo.
echo To upload to Test PyPI (wheels only):
echo   python -m twine upload --repository testpypi dist/*.whl
echo.
echo To upload to PyPI (wheels only):
echo   python -m twine upload dist/*.whl
echo.
echo DO NOT upload the .tar.gz file!
echo.
pause

