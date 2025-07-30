@echo off
REM Smart MCP Dispatcher Installation Script for Windows
REM This script installs the MCP dispatcher tools system-wide

echo Smart MCP Dispatcher - Windows Installation
echo ==========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in PATH
    echo Please install pip
    pause
    exit /b 1
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)

REM Create Scripts directory if it doesn't exist
if not exist "%USERPROFILE%\Scripts" (
    mkdir "%USERPROFILE%\Scripts"
)

REM Copy scripts to user Scripts directory
echo Installing MCP dispatcher scripts...
copy mcp_dispatcher.py "%USERPROFILE%\Scripts\"
copy mcp_proxy.py "%USERPROFILE%\Scripts\"

REM Create batch wrapper for mcp-dispatcher
echo @echo off > "%USERPROFILE%\Scripts\mcp-dispatcher.bat"
echo python "%%USERPROFILE%%\Scripts\mcp_dispatcher.py" %%* >> "%USERPROFILE%\Scripts\mcp-dispatcher.bat"

REM Create batch wrapper for mcp-proxy
echo @echo off > "%USERPROFILE%\Scripts\mcp-proxy.bat"
echo python "%%USERPROFILE%%\Scripts\mcp_proxy.py" %%* >> "%USERPROFILE%\Scripts\mcp-proxy.bat"

REM Check if Scripts directory is in PATH
echo %PATH% | findstr /i "%USERPROFILE%\Scripts" >nul
if errorlevel 1 (
    echo.
    echo WARNING: %USERPROFILE%\Scripts is not in your PATH
    echo Please add it to your PATH environment variable to use the commands globally:
    echo.
    echo 1. Open System Properties ^(Win+R, type sysdm.cpl^)
    echo 2. Click "Environment Variables"
    echo 3. Under "User variables", select "Path" and click "Edit"
    echo 4. Click "New" and add: %USERPROFILE%\Scripts
    echo 5. Click OK and restart your command prompt
    echo.
    echo Alternatively, you can run:
    echo setx PATH "%%PATH%%;%USERPROFILE%\Scripts"
    echo.
    pause
) else (
    echo Scripts directory is already in PATH
)

echo.
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Run: setup.py (to configure your MCP servers)
echo 2. Test: mcp-dispatcher test
echo 3. Configure Claude Code with the proxy
echo.
pause