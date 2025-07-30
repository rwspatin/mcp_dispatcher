#!/usr/bin/env python3
"""
Smart MCP Dispatcher Setup Script

This script helps users configure their MCP dispatcher by:
1. Creating config.json from template
2. Guiding user through basic configuration
3. Validating the configuration
"""

import json
import os
import sys
import platform
from pathlib import Path

def get_platform_info():
    """Get platform-specific information"""
    system = platform.system().lower()
    
    if system == "windows":
        return {
            "name": "Windows",
            "python_cmd": "python",
            "path_examples": [
                "C:/Users/*/projects/web*",
                "C:/projects/nodejs*",
                "D:/development/*"
            ],
            "default_python_path": "C:/path/to/your/mcp/server.py"
        }
    elif system == "darwin":
        return {
            "name": "macOS", 
            "python_cmd": "python3",
            "path_examples": [
                "/Users/*/projects/web*",
                "/Users/*/Development/nodejs*",
                "/Applications/*/mcp-projects*"
            ],
            "default_python_path": "/path/to/your/mcp/server.py"
        }
    else:
        return {
            "name": "Linux",
            "python_cmd": "python3", 
            "path_examples": [
                "/home/*/projects/web*",
                "/home/*/development/nodejs*",
                "/opt/projects/*"
            ],
            "default_python_path": "/path/to/your/mcp/server.py"
        }

def main():
    platform_info = get_platform_info()
    
    print(f"🚀 Smart MCP Dispatcher Setup ({platform_info['name']})")
    print("=" * 50)
    
    # Check if config already exists
    if os.path.exists("config.json"):
        response = input("config.json already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Check if template exists
    if not os.path.exists("config.json.template"):
        print("❌ config.json.template not found!")
        print("Please ensure you're running this from the project directory.")
        sys.exit(1)
    
    # Load template
    with open("config.json.template", 'r') as f:
        config = json.load(f)
    
    print(f"\n📝 Let's configure your MCP dispatcher for {platform_info['name']}...")
    print("You need to provide:")
    print("1. At least one project path mapping")
    print("2. A default MCP server")
    print()
    print(f"💡 Example path patterns for {platform_info['name']}:")
    for example in platform_info['path_examples']:
        print(f"   • {example}")
    print()
    
    # Get user input for default server
    print("🔧 Default MCP Server Configuration:")
    default_name = input("Default MCP server name (default-mcp): ").strip() or "default-mcp"
    default_command = input(f"Command to run ({platform_info['python_cmd']}/node/path-to-binary): ").strip()
    if not default_command:
        print("❌ Command is required!")
        sys.exit(1)
    
    default_args = input("Arguments (e.g., /path/to/server.py): ").strip()
    default_args_list = [default_args] if default_args else []
    
    default_desc = input("Description (optional): ").strip() or f"Default {default_command} MCP Server"
    
    # Update default server in config
    config["default_mcp_server"] = {
        "name": default_name,
        "command": default_command,
        "args": default_args_list,
        "description": default_desc
    }
    
    # Get user input for first path mapping
    print("\n🗂️  First Project Path Mapping:")
    path_pattern = input("Path pattern (e.g., /home/*/projects/web-dev*): ").strip()
    if not path_pattern:
        print("❌ Path pattern is required!")
        sys.exit(1)
    
    mapping_name = input("MCP server name for this path: ").strip()
    if not mapping_name:
        print("❌ MCP server name is required!")
        sys.exit(1)
    
    mapping_command = input("Command to run (python/node/path-to-binary): ").strip()
    if not mapping_command:
        print("❌ Command is required!")
        sys.exit(1)
    
    mapping_args = input("Arguments (e.g., /path/to/server.py): ").strip()
    mapping_args_list = [mapping_args] if mapping_args else []
    
    mapping_desc = input("Description (optional): ").strip() or f"{mapping_name} MCP Server"
    
    # Update first mapping in config
    config["path_mappings"] = [{
        "path_pattern": path_pattern,
        "mcp_server": {
            "name": mapping_name,
            "command": mapping_command,
            "args": mapping_args_list,
            "description": mapping_desc
        }
    }]
    
    # Ask if they want to add more mappings
    while True:
        add_more = input("\n➕ Add another path mapping? (y/N): ").strip().lower()
        if add_more != 'y':
            break
            
        print("\n🗂️  Additional Project Path Mapping:")
        path_pattern = input("Path pattern: ").strip()
        if not path_pattern:
            continue
            
        mapping_name = input("MCP server name: ").strip()
        if not mapping_name:
            continue
            
        mapping_command = input("Command to run: ").strip()
        if not mapping_command:
            continue
            
        mapping_args = input("Arguments (optional): ").strip()
        mapping_args_list = [mapping_args] if mapping_args else []
        
        mapping_desc = input("Description (optional): ").strip() or f"{mapping_name} MCP Server"
        
        config["path_mappings"].append({
            "path_pattern": path_pattern,
            "mcp_server": {
                "name": mapping_name,
                "command": mapping_command,
                "args": mapping_args_list,
                "description": mapping_desc
            }
        })
    
    # Save configuration
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved to config.json")
    print("\n🧪 Testing your configuration...")
    
    # Test configuration
    from mcp_dispatcher import MCPDispatcher
    try:
        dispatcher = MCPDispatcher("config.json")
        print("✅ Configuration is valid!")
        
        print("\n📋 Your current mappings:")
        dispatcher.list_mappings()
        
        print("\n🎉 Setup complete!")
        print("You can now use:")
        print("  mcp-dispatcher test    # Test current directory")
        print("  mcp-dispatcher list    # List all mappings") 
        print("  mcp-dispatcher add ... # Add more mappings")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your paths and commands.")
        sys.exit(1)

if __name__ == "__main__":
    main()