#!/usr/bin/env python3
"""
Smart MCP Dispatcher - Dynamically chooses which MCP server to use based on current directory path.

This dispatcher allows you to:
- Map directory paths to specific MCP servers
- Automatically route requests to the appropriate MCP server based on current working directory
- Manage path mappings via CLI
- Proxy MCP requests transparently
"""

import json
import os
import sys
import subprocess
import argparse
import fnmatch
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

class MCPDispatcher:
    def __init__(self, config_file: str = None):
        # Priority order: explicit config_file -> MCP_DISPATCHER_CONFIG env var -> local config.json -> default config
        if config_file:
            self.config_file = config_file
        elif os.environ.get("MCP_DISPATCHER_CONFIG"):
            self.config_file = os.environ.get("MCP_DISPATCHER_CONFIG")
        elif os.path.exists("config.json"):
            self.config_file = "config.json"
        else:
            self.config_file = self._get_default_config_path()
        
        self.config = self._load_config()
        self.logger = self._setup_logging()
    
    def _get_default_config_path(self) -> str:
        """Get platform-specific default config path"""
        system = platform.system().lower()
        
        if system == "windows":
            # Windows: Use APPDATA
            appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
            return os.path.join(appdata, "mcp_dispatcher", "config.json")
        elif system == "darwin":
            # macOS: Use Application Support
            return os.path.expanduser("~/Library/Application Support/mcp_dispatcher/config.json")
        else:
            # Linux/Unix: Use .config or home
            config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            return os.path.join(config_dir, "mcp_dispatcher", "config.json")
    
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('mcp_dispatcher')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            self._show_config_error()
            sys.exit(1)
            
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            # Validate configuration
            if not self._validate_config(config):
                sys.exit(1)
                
            return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error loading config file '{self.config_file}': {e}")
            print("Please check your configuration file syntax and try again.")
            sys.exit(1)
    
    def _show_config_error(self):
        """Show helpful error message when config is missing"""
        print("❌ Configuration file not found!")
        print(f"Expected location: {self.config_file}")
        print()
        print("🔧 To get started:")
        print("1. Run the setup script: ./setup.py")
        print("2. Or copy the template: cp config.json.template config.json")
        print("3. Edit config.json with your MCP server paths")
        print()
        print("📖 You must configure AT LEAST:")
        print("   - One path mapping for your projects")
        print("   - A default MCP server")
        print()
        print("📚 See README.md for configuration examples")
    
    def _validate_config(self, config: Dict) -> bool:
        """Validate configuration has required fields"""
        errors = []
        
        # Check for default server
        if "default_mcp_server" not in config:
            errors.append("Missing 'default_mcp_server' configuration")
        else:
            default_server = config["default_mcp_server"]
            if not all(key in default_server for key in ["name", "command", "args"]):
                errors.append("default_mcp_server must have 'name', 'command', and 'args'")
        
        # Check path mappings exist
        if "path_mappings" not in config:
            errors.append("Missing 'path_mappings' configuration")
        elif not config["path_mappings"]:
            errors.append("At least one path mapping is required")
        else:
            # Validate each mapping
            for i, mapping in enumerate(config["path_mappings"]):
                if "path_pattern" not in mapping:
                    errors.append(f"path_mappings[{i}] missing 'path_pattern'")
                if "mcp_server" not in mapping:
                    errors.append(f"path_mappings[{i}] missing 'mcp_server'")
                elif not all(key in mapping["mcp_server"] for key in ["name", "command", "args"]):
                    errors.append(f"path_mappings[{i}].mcp_server must have 'name', 'command', and 'args'")
        
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   • {error}")
            print()
            print("📚 See README.md for configuration examples")
            return False
            
        return True
    
    def _save_config(self):
        """Save configuration to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except IOError as e:
            self.logger.error(f"Error saving config: {e}")
    
    def find_matching_server(self, current_path: str = None) -> Dict:
        """Find the MCP server that matches the current directory path"""
        if current_path is None:
            current_path = os.getcwd()
        
        current_path = os.path.abspath(current_path)
        # Normalize path separators for cross-platform compatibility
        current_path = self._normalize_path(current_path)
        self.logger.info(f"Looking for MCP server for path: {current_path}")
        
        # Check each path mapping
        for mapping in self.config.get("path_mappings", []):
            pattern = mapping["path_pattern"]
            normalized_pattern = self._normalize_path(pattern)
            if fnmatch.fnmatch(current_path, normalized_pattern):
                self.logger.info(f"Matched pattern '{pattern}' -> {mapping['mcp_server']['name']}")
                return mapping["mcp_server"]
        
        # Return default server if no match found
        default_server = self.config.get("default_mcp_server")
        self.logger.info(f"No pattern matched, using default: {default_server['name']}")
        return default_server
    
    def _normalize_path(self, path: str) -> str:
        """Normalize path for cross-platform compatibility"""
        # Convert to forward slashes for consistent pattern matching
        # fnmatch works with forward slashes on all platforms
        return path.replace(os.sep, '/')
    
    def add_path_mapping(self, path_pattern: str, server_name: str, command: str, args: List[str], description: str = ""):
        """Add a new path mapping"""
        new_mapping = {
            "path_pattern": path_pattern,
            "mcp_server": {
                "name": server_name,
                "command": command,
                "args": args,
                "description": description
            }
        }
        
        if "path_mappings" not in self.config:
            self.config["path_mappings"] = []
        
        self.config["path_mappings"].append(new_mapping)
        self._save_config()
        self.logger.info(f"Added mapping: {path_pattern} -> {server_name}")
    
    def remove_path_mapping(self, path_pattern: str) -> bool:
        """Remove a path mapping"""
        if "path_mappings" not in self.config:
            return False
        
        original_count = len(self.config["path_mappings"])
        self.config["path_mappings"] = [
            mapping for mapping in self.config["path_mappings"]
            if mapping["path_pattern"] != path_pattern
        ]
        
        if len(self.config["path_mappings"]) < original_count:
            self._save_config()
            self.logger.info(f"Removed mapping for pattern: {path_pattern}")
            return True
        return False
    
    def list_mappings(self):
        """List all path mappings"""
        print("Current MCP Path Mappings:")
        print("=" * 50)
        
        if "path_mappings" in self.config and self.config["path_mappings"]:
            for i, mapping in enumerate(self.config["path_mappings"], 1):
                server = mapping["mcp_server"]
                print(f"{i}. Pattern: {mapping['path_pattern']}")
                print(f"   Server: {server['name']}")
                print(f"   Command: {server['command']} {' '.join(server['args'])}")
                print(f"   Description: {server.get('description', 'N/A')}")
                print()
        else:
            print("No path mappings configured.")
        
        print("Default Server:")
        default = self.config.get("default_mcp_server", {})
        print(f"   Server: {default.get('name', 'N/A')}")
        print(f"   Command: {default.get('command', 'N/A')} {' '.join(default.get('args', []))}")
        print(f"   Description: {default.get('description', 'N/A')}")
    
    def test_current_path(self, test_path: str = None):
        """Test which server would be selected for current or specified path"""
        current_path = test_path or os.getcwd()
        server = self.find_matching_server(current_path)
        
        print(f"Path: {current_path}")
        print(f"Selected MCP Server: {server['name']}")
        print(f"Command: {server['command']} {' '.join(server['args'])}")
        print(f"Description: {server.get('description', 'N/A')}")
    
    def start_server(self, path: str = None):
        """Start the appropriate MCP server for the current or specified path"""
        server = self.find_matching_server(path)
        
        print(f"Starting MCP server: {server['name']}")
        print(f"Command: {server['command']} {' '.join(server['args'])}")
        
        try:
            # Execute the MCP server command
            cmd = [server['command']] + server['args']
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error starting MCP server: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            self.logger.error(f"MCP server command not found: {e}")
            sys.exit(1)
    
    def enable_in_current_directory(self):
        """Enable MCP dispatcher in current directory by copying .mcp.json"""
        current_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        source_mcp_config = os.path.join(script_dir, ".mcp.json")
        target_mcp_config = os.path.join(current_dir, ".mcp.json")
        
        print(f"🚀 Enabling MCP dispatcher in: {current_dir}")
        
        # Check if source .mcp.json exists
        if not os.path.exists(source_mcp_config):
            print(f"❌ Error: {source_mcp_config} not found!")
            print("Please ensure .mcp.json exists in the MCP dispatcher directory.")
            return False
        
        # Check if target already exists
        if os.path.exists(target_mcp_config):
            response = input(f"⚠️  .mcp.json already exists in {current_dir}. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("❌ Operation cancelled.")
                return False
        
        try:
            # Copy the .mcp.json file
            import shutil
            shutil.copy2(source_mcp_config, target_mcp_config)
            print(f"✅ MCP configuration copied successfully!")
            print(f"📁 Location: {target_mcp_config}")
            print()
            print("🎉 MCP dispatcher is now enabled in this directory!")
            print("💡 You can now use Claude Code with MCP tools in this project.")
            print("🧪 Test it with: mcp-dispatcher test")
            return True
            
        except Exception as e:
            print(f"❌ Error copying MCP configuration: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Smart MCP Dispatcher")
    parser.add_argument("--config", help="Configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add mapping command
    add_parser = subparsers.add_parser("add", help="Add a new path mapping")
    add_parser.add_argument("pattern", help="Path pattern (supports wildcards)")
    add_parser.add_argument("name", help="MCP server name")
    add_parser.add_argument("command", help="Command to run MCP server")
    add_parser.add_argument("args", nargs="*", help="Arguments for MCP server command")
    add_parser.add_argument("--description", help="Description of the MCP server")
    
    # Remove mapping command
    remove_parser = subparsers.add_parser("remove", help="Remove a path mapping")
    remove_parser.add_argument("pattern", help="Path pattern to remove")
    
    # List mappings command
    subparsers.add_parser("list", help="List all path mappings")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test which server would be selected")
    test_parser.add_argument("--path", help="Path to test (defaults to current directory)")
    
    # Start server command
    start_parser = subparsers.add_parser("start", help="Start the appropriate MCP server")
    start_parser.add_argument("--path", help="Path to determine server (defaults to current directory)")
    
    # Help command
    subparsers.add_parser("help", help="Show help information")
    
    # Enable MCP in current directory
    subparsers.add_parser("enable", help="Enable MCP dispatcher in current directory")
    
    # Test installation
    test_parser = subparsers.add_parser("test-install", help="Test MCP dispatcher installation")
    test_parser.add_argument("--quick", action="store_true", help="Run only essential tests")
    test_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    dispatcher = MCPDispatcher(args.config)
    
    if args.command == "add":
        dispatcher.add_path_mapping(
            args.pattern, 
            args.name, 
            args.command, 
            args.args, 
            args.description or ""
        )
        print(f"Added mapping: {args.pattern} -> {args.name}")
    
    elif args.command == "remove":
        if dispatcher.remove_path_mapping(args.pattern):
            print(f"Removed mapping for pattern: {args.pattern}")
        else:
            print(f"No mapping found for pattern: {args.pattern}")
    
    elif args.command == "list":
        dispatcher.list_mappings()
    
    elif args.command == "test":
        dispatcher.test_current_path(args.path)
    
    elif args.command == "start":
        dispatcher.start_server(args.path)
    
    elif args.command == "help":
        parser.print_help()
    
    elif args.command == "enable":
        dispatcher.enable_in_current_directory()
    
    elif args.command == "test-install":
        # Run the comprehensive test suite
        test_script = os.path.join(os.path.dirname(__file__), "test_mcp_dispatcher.py")
        if not os.path.exists(test_script):
            print("❌ Test script not found. Please ensure test_mcp_dispatcher.py is in the same directory.")
            sys.exit(1)
        
        # Build test command
        test_cmd = [sys.executable, test_script]
        if args.quick:
            test_cmd.append("--quick")
        if args.verbose:
            test_cmd.append("--verbose")
        
        # Run tests
        try:
            result = subprocess.run(test_cmd, check=False)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()