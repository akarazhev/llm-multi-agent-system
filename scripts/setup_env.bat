@echo off

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Get the project root directory (one level up from scripts)
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Create Python virtual environment in project root using Python 3.12
python -m venv "%PROJECT_ROOT%\.venv"
if errorlevel 1 (
    echo Failed to create virtual environment
    exit /b 1
)

REM Activate environment
call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)

REM Install the package in editable mode
pip install --force-reinstall -e .
if errorlevel 1 (
    echo Failed to install business_analyst_agent package
    exit /b 1
)

REM Verify installation
pip show business_analyst_agent
if errorlevel 1 (
    echo Package installation verification failed
    exit /b 1
)

echo Environment setup complete. Activate with:
echo call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
echo To run the agent: ba-agent
