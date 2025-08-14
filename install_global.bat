@echo off
REM Smart MCP Dispatcher - Global Installation Script for Windows
REM This script installs the MCP dispatcher globally for Claude Code

setlocal enabledelayedexpansion

echo.
echo 🚀 Smart MCP Dispatcher - Global Installation (Windows)
echo.

REM Check prerequisites
echo 📋 Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Claude Code CLI
claude --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Claude Code CLI not found in PATH
    echo    Installation will continue, but you'll need to configure manually
    set CLAUDE_CLI_AVAILABLE=false
) else (
    echo ✅ Claude Code CLI found
    set CLAUDE_CLI_AVAILABLE=true
)

echo.

REM Step 1: Run setup if config doesn't exist
echo 📝 Step 1: Configuration Setup
if not exist "config.json" (
    echo Running interactive setup...
    python setup.py
    if errorlevel 1 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
) else (
    echo ✅ Configuration file already exists
)

REM Step 2: Install binaries
echo.
echo 🔧 Step 2: Installing Binaries
call install.bat
if errorlevel 1 (
    echo ❌ Binary installation failed
    pause
    exit /b 1
)

set BINARY_PATH=%USERPROFILE%\Scripts\mcp-dispatcher-exec
set CONFIG_PATH=%cd%\config.json

REM Step 3: Configure Claude Code
echo.
echo ⚙️  Step 3: Claude Code Configuration

if "!CLAUDE_CLI_AVAILABLE!"=="true" (
    echo Configuring Claude Code globally...
    claude mcp add smart-mcp-dispatcher --scope user "!BINARY_PATH!" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Claude CLI configuration failed, will show manual instructions
        set CLAUDE_CONFIGURED=false
    ) else (
        echo ✅ Claude Code configured successfully using CLI
        set CLAUDE_CONFIGURED=true
    )
) else (
    set CLAUDE_CONFIGURED=false
)

REM Step 4: Manual configuration instructions if needed
if "!CLAUDE_CONFIGURED!"=="false" (
    echo.
    echo 📖 Manual Configuration Required
    echo.
    echo Please add the following to your Claude Code configuration:
    echo.
    echo Configuration file location: %%APPDATA%%\ClaudeCode\config.json
    echo.
    echo Configuration to add:
    echo {
    echo   "mcp": {
    echo     "servers": {
    echo       "smart-mcp-dispatcher": {
    echo         "command": "!BINARY_PATH!",
    echo         "args": [],
    echo         "env": {
    echo           "MCP_DISPATCHER_CONFIG": "!CONFIG_PATH!"
    echo         }
    echo       }
    echo     }
    echo   }
    echo }
    echo.
)

REM Step 5: Test installation
echo.
echo 🧪 Step 5: Testing Installation

mcp-dispatcher test >nul 2>&1
if errorlevel 1 (
    echo ❌ MCP Dispatcher test failed
    echo Check your configuration and try: mcp-dispatcher test
) else (
    echo ✅ MCP Dispatcher test successful
)

REM Step 6: Final instructions
echo.
echo 🎉 Installation Complete!
echo.
echo What's Next:
echo 1. Test different directories: cd to various project folders and run "mcp-dispatcher test"
echo 2. Add more mappings: Use "mcp-dispatcher add" to configure more project paths
echo 3. List current setup: Run "mcp-dispatcher list" to see all configured servers

if "!CLAUDE_CONFIGURED!"=="false" (
    echo 4. Configure Claude Code: Follow the manual configuration instructions above
    echo 5. Restart Claude Code for changes to take effect
) else (
    echo 4. Restart Claude Code for changes to take effect
)

echo.
echo The Smart MCP Dispatcher is now installed globally!
echo It will automatically route to the correct MCP server based on your directory.
echo.

pause