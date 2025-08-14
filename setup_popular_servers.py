#!/usr/bin/env python3
"""
Automated setup script for popular MCP servers
This script helps users quickly configure common MCP servers with the Smart MCP Dispatcher
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from mcp_dispatcher import MCPDispatcher

def check_command_available(command: str) -> bool:
    """Check if a command is available in PATH"""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default"""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    else:
        return input(f"{prompt}: ").strip()

def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response.startswith('y')

def setup_zen_mcp(dispatcher: MCPDispatcher) -> bool:
    """Setup Zen MCP Server"""
    print("\n🧠 Setting up Zen MCP Server...")
    print("   Multi-AI orchestration with guided workflows")
    
    if not get_yes_no("Install Zen MCP Server?", True):
        return False
    
    # Check if npx is available
    if not check_command_available('npx'):
        print("❌ npm/npx not found. Please install Node.js first.")
        return False
    
    # Get API keys
    print("\n🔑 Zen MCP requires API keys for external AI models:")
    gemini_key = get_user_input("Gemini API Key (optional, for Gemini models)")
    openai_key = get_user_input("OpenAI API Key (optional, for GPT models)")
    
    # Prepare environment variables
    env_vars = {}
    if gemini_key:
        env_vars["GEMINI_API_KEY"] = gemini_key
    if openai_key:
        env_vars["OPENAI_API_KEY"] = openai_key
    
    # Add Zen MCP as default server
    zen_config = {
        "name": "zen-mcp",
        "command": "npx",
        "args": ["zen-mcp-server-199bio"],
        "description": "Zen MCP Server - Multi-AI orchestration with guided workflows"
    }
    
    if env_vars:
        zen_config["env"] = env_vars
    
    dispatcher.config["default_mcp_server"] = zen_config
    
    # Add path mapping for general development
    dispatcher.add_path_mapping(
        "/home/*/dev*",
        "zen-mcp",
        "npx",
        ["zen-mcp-server-199bio"],
        "Zen MCP for development projects"
    )
    
    print("✅ Zen MCP Server configured as default")
    return True

def setup_filesystem_mcp(dispatcher: MCPDispatcher) -> bool:
    """Setup Filesystem MCP"""
    print("\n💻 Setting up Filesystem MCP...")
    print("   Essential file and directory operations")
    
    if not get_yes_no("Install Filesystem MCP?", True):
        return False
    
    # Check if npx is available
    if not check_command_available('npx'):
        print("❌ npm/npx not found. Please install Node.js first.")
        return False
    
    # Get allowed directories
    home_dir = os.path.expanduser("~")
    allowed_dir = get_user_input("Directory to allow filesystem access", home_dir)
    
    # Add filesystem mapping for development directories
    dispatcher.add_path_mapping(
        f"{allowed_dir}/projects*",
        "filesystem-mcp",
        "npx",
        ["@modelcontextprotocol/server-filesystem", allowed_dir],
        "Filesystem operations for projects"
    )
    
    print("✅ Filesystem MCP configured")
    return True

def setup_git_mcp(dispatcher: MCPDispatcher) -> bool:
    """Setup Git MCP"""
    print("\n🛠️ Setting up Git MCP...")
    print("   Git repository operations and analysis")
    
    if not get_yes_no("Install Git MCP?", True):
        return False
    
    # Check if git and npx are available
    if not check_command_available('git'):
        print("❌ git not found. Please install Git first.")
        return False
    
    if not check_command_available('npx'):
        print("❌ npm/npx not found. Please install Node.js first.")
        return False
    
    # Get repository directory
    home_dir = os.path.expanduser("~")
    git_dir = get_user_input("Git repositories directory", f"{home_dir}/projects")
    
    # Add git mapping
    dispatcher.add_path_mapping(
        f"{git_dir}*",
        "git-mcp",
        "npx",
        ["@modelcontextprotocol/server-git", "--repository", git_dir],
        "Git operations for repositories"
    )
    
    print("✅ Git MCP configured")
    return True

def setup_browser_mcp(dispatcher: MCPDispatcher) -> bool:
    """Setup Browser MCP"""
    print("\n🌐 Setting up Browser MCP...")
    print("   Web page interaction and automation")
    
    if not get_yes_no("Install Browser MCP?", False):
        return False
    
    # Check if npx is available
    if not check_command_available('npx'):
        print("❌ npm/npx not found. Please install Node.js first.")
        return False
    
    # Add browser mapping for web development
    dispatcher.add_path_mapping(
        "/home/*/web*",
        "browser-mcp",
        "npx",
        ["@modelcontextprotocol/server-browser"],
        "Browser automation for web projects"
    )
    
    print("✅ Browser MCP configured")
    return True

def setup_sqlite_mcp(dispatcher: MCPDispatcher) -> bool:
    """Setup SQLite MCP"""
    print("\n📊 Setting up SQLite MCP...")
    print("   Database operations and analysis")
    
    if not get_yes_no("Install SQLite MCP?", False):
        return False
    
    # Check if npx is available
    if not check_command_available('npx'):
        print("❌ npm/npx not found. Please install Node.js first.")
        return False
    
    # Get database directory
    home_dir = os.path.expanduser("~")
    db_dir = get_user_input("Database directory", f"{home_dir}/databases")
    
    # Add SQLite mapping
    dispatcher.add_path_mapping(
        f"{db_dir}*",
        "sqlite-mcp",
        "npx",
        ["@modelcontextprotocol/server-sqlite"],
        "SQLite operations for databases"
    )
    
    print("✅ SQLite MCP configured")
    return True

def main():
    """Main setup function"""
    print("🚀 Smart MCP Dispatcher - Popular Servers Setup")
    print("=" * 60)
    print()
    print("This script will help you quickly set up popular MCP servers.")
    print("You can always add more servers later using 'mcp-dispatcher add'.")
    print()
    
    try:
        # Initialize dispatcher
        dispatcher = MCPDispatcher()
        
        # Load existing config or create new one
        if not os.path.exists(dispatcher.config_file):
            print(f"Creating new configuration at: {dispatcher.config_file}")
            dispatcher.config = {
                "path_mappings": [],
                "default_mcp_server": {},
                "logging": {
                    "level": "INFO",
                    "file": "/tmp/mcp_dispatcher.log"
                }
            }
        
        print(f"📁 Configuration file: {dispatcher.config_file}")
        print()
        
        # Setup popular servers
        servers_configured = 0
        
        if setup_zen_mcp(dispatcher):
            servers_configured += 1
        
        if setup_filesystem_mcp(dispatcher):
            servers_configured += 1
        
        if setup_git_mcp(dispatcher):
            servers_configured += 1
        
        if setup_browser_mcp(dispatcher):
            servers_configured += 1
        
        if setup_sqlite_mcp(dispatcher):
            servers_configured += 1
        
        # Save configuration
        if servers_configured > 0:
            dispatcher._save_config()
            print(f"\n✅ Configuration saved with {servers_configured} MCP servers!")
            
            # Show summary
            print("\n📋 Configuration Summary:")
            dispatcher.list_mappings()
            
            # Test installation
            print(f"\n🧪 Testing installation...")
            try:
                subprocess.run([sys.executable, "-c", "from mcp_dispatcher import MCPDispatcher; print('✅ Dispatcher working')"], check=True)
                print("✅ Installation test passed!")
            except Exception as e:
                print(f"⚠️  Installation test warning: {e}")
            
            print(f"\n🎉 Setup complete!")
            print(f"💡 Next steps:")
            print(f"   1. Test your setup: mcp-dispatcher test-install")
            print(f"   2. Test path routing: mcp-dispatcher test")
            print(f"   3. Add more servers: mcp-dispatcher add")
            print(f"   4. List all servers: mcp-dispatcher list")
        else:
            print("\n❌ No servers were configured.")
            print("Run this script again or use 'mcp-dispatcher add' to configure servers manually.")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()