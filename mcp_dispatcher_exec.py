#!/usr/bin/env python3
"""
MCP Dispatcher Exec - Direct execution wrapper for Claude Code
This script determines which MCP server to run based on current directory
and then directly executes it (replacing the current process)
"""

import os
import sys
import json
import subprocess
import fnmatch

def normalize_path(path: str) -> str:
    """Normalize path for cross-platform compatibility"""
    return path.replace(os.sep, '/')

def load_config():
    """Load MCP dispatcher configuration"""
    # Try to find config file
    config_file = None
    
    if os.environ.get("MCP_DISPATCHER_CONFIG"):
        config_file = os.environ.get("MCP_DISPATCHER_CONFIG")
    elif os.path.exists("config.json"):
        config_file = "config.json"
    elif os.path.exists(os.path.expanduser("~/.config/mcp_dispatcher/config.json")):
        config_file = os.path.expanduser("~/.config/mcp_dispatcher/config.json")
    
    if not config_file or not os.path.exists(config_file):
        print(f"❌ Configuration file not found!", file=sys.stderr)
        print(f"Set MCP_DISPATCHER_CONFIG environment variable or create config.json", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}", file=sys.stderr)
        sys.exit(1)

def find_matching_server(config, current_path=None):
    """Find the MCP server that matches the current directory path"""
    if current_path is None:
        current_path = os.getcwd()
    
    current_path = os.path.abspath(current_path)
    current_path = normalize_path(current_path)
    
    # Check each path mapping
    for mapping in config.get("path_mappings", []):
        pattern = mapping["path_pattern"]
        normalized_pattern = normalize_path(pattern)
        if fnmatch.fnmatch(current_path, normalized_pattern):
            return mapping["mcp_server"]
    
    # Return default server if no match found
    return config.get("default_mcp_server")

def main():
    """Main function to determine and execute the appropriate MCP server"""
    try:
        # Load configuration
        config = load_config()
        
        # Get the appropriate server for current directory
        server_config = find_matching_server(config)
        
        if not server_config:
            print("❌ No MCP server configured", file=sys.stderr)
            sys.exit(1)
        
        # Prepare command
        cmd = [server_config['command']] + server_config['args']
        
        # Prepare environment - this is critical!
        env = os.environ.copy()
        if 'env' in server_config:
            env.update(server_config['env'])
        
        # Debug logging
        print(f"🚀 Starting MCP server: {server_config['name']}", file=sys.stderr)
        print(f"📂 Working directory: {os.getcwd()}", file=sys.stderr)
        print(f"💻 Command: {' '.join(cmd)}", file=sys.stderr)
        
        # Execute the MCP server by replacing current process
        os.execvpe(cmd[0], cmd, env)
        
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()