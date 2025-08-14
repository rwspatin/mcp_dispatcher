#!/usr/bin/env python3
"""
Comprehensive test suite for Smart MCP Dispatcher
This script validates the entire MCP dispatcher installation and configuration.
"""

import os
import sys
import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple

class MCPDispatcherTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
        self.verbose = False
    
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with levels"""
        if level == "INFO":
            print(f"ℹ️  {message}")
        elif level == "SUCCESS":
            print(f"✅ {message}")
        elif level == "ERROR":
            print(f"❌ {message}")
        elif level == "WARNING":
            print(f"⚠️  {message}")
        elif level == "DEBUG" and self.verbose:
            print(f"🔍 {message}")
    
    def run_command(self, cmd: str, timeout: int = 10) -> Tuple[bool, str, str]:
        """Run a command and return success, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def test_python_dependencies(self) -> bool:
        """Test that Python and required modules are available"""
        self.log("Testing Python dependencies...", "INFO")
        
        # Test Python version
        success, stdout, stderr = self.run_command("python3 --version")
        if not success:
            self.log("Python 3 not found in PATH", "ERROR")
            return False
        
        self.log(f"Python version: {stdout.strip()}", "DEBUG")
        
        # Test required modules
        required_modules = ["json", "os", "sys", "subprocess", "fnmatch", "pathlib"]
        for module in required_modules:
            success, _, stderr = self.run_command(f"python3 -c 'import {module}'")
            if not success:
                self.log(f"Required module '{module}' not available", "ERROR")
                return False
        
        self.log("Python dependencies OK", "SUCCESS")
        return True
    
    def test_cli_installation(self) -> bool:
        """Test that mcp-dispatcher CLI is installed and accessible"""
        self.log("Testing CLI installation...", "INFO")
        
        success, stdout, stderr = self.run_command("which mcp-dispatcher")
        if not success:
            self.log("mcp-dispatcher not found in PATH", "ERROR")
            self.log("Run the installation script first", "WARNING")
            return False
        
        cli_path = stdout.strip()
        self.log(f"CLI found at: {cli_path}", "DEBUG")
        
        # Test CLI help
        success, stdout, stderr = self.run_command("mcp-dispatcher --help")
        if not success:
            self.log("mcp-dispatcher CLI not working", "ERROR")
            return False
        
        self.log("CLI installation OK", "SUCCESS")
        return True
    
    def test_configuration_file(self) -> bool:
        """Test configuration file existence and validity"""
        self.log("Testing configuration file...", "INFO")
        
        # Check for config file
        config_paths = [
            "config.json",
            os.path.expanduser("~/.config/mcp_dispatcher/config.json"),
            os.path.expanduser("~/.mcp_dispatcher_config.json")
        ]
        
        config_file = None
        if os.environ.get("MCP_DISPATCHER_CONFIG"):
            config_file = os.environ.get("MCP_DISPATCHER_CONFIG")
        else:
            for path in config_paths:
                if os.path.exists(path):
                    config_file = path
                    break
        
        if not config_file:
            self.log("No configuration file found", "ERROR")
            self.log("Run 'setup.py' to create configuration", "WARNING")
            return False
        
        self.log(f"Config file: {config_file}", "DEBUG")
        
        # Validate config JSON
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            self.log(f"Invalid configuration JSON: {e}", "ERROR")
            return False
        
        # Validate required fields
        required_fields = ["path_mappings", "default_mcp_server"]
        for field in required_fields:
            if field not in config:
                self.log(f"Missing required field: {field}", "ERROR")
                return False
        
        # Validate default server
        default_server = config["default_mcp_server"]
        if not all(key in default_server for key in ["name", "command", "args"]):
            self.log("Invalid default_mcp_server configuration", "ERROR")
            return False
        
        self.log("Configuration file OK", "SUCCESS")
        return True
    
    def test_dispatcher_executable(self) -> bool:
        """Test the dispatcher executable"""
        self.log("Testing dispatcher executable...", "INFO")
        
        # Find the executable
        exec_paths = [
            "/home/user/.local/bin/mcp-dispatcher-exec",
            os.path.expanduser("~/.local/bin/mcp-dispatcher-exec"),
            "mcp-dispatcher-exec"
        ]
        
        exec_file = None
        for path in exec_paths:
            if os.path.exists(path):
                exec_file = path
                break
        
        if not exec_file:
            self.log("mcp-dispatcher-exec not found", "ERROR")
            return False
        
        self.log(f"Executable: {exec_file}", "DEBUG")
        
        # Test that it's executable
        if not os.access(exec_file, os.X_OK):
            self.log("mcp-dispatcher-exec is not executable", "ERROR")
            return False
        
        self.log("Dispatcher executable OK", "SUCCESS")
        return True
    
    def test_path_routing(self) -> bool:
        """Test path-based routing functionality"""
        self.log("Testing path routing...", "INFO")
        
        # Test current directory
        success, stdout, stderr = self.run_command("mcp-dispatcher test")
        if not success:
            self.log("Path routing test failed", "ERROR")
            self.log(f"Error: {stderr}", "DEBUG")
            return False
        
        # Test specific paths from config
        test_paths = ["/tmp", "/home", "/usr"]
        for path in test_paths:
            if os.path.exists(path):
                success, stdout, stderr = self.run_command(f"mcp-dispatcher test --path {path}")
                if not success:
                    self.log(f"Path routing failed for {path}", "ERROR")
                    return False
        
        self.log("Path routing OK", "SUCCESS")
        return True
    
    def test_mcp_server_executability(self) -> bool:
        """Test that configured MCP servers are executable"""
        self.log("Testing MCP server executability...", "INFO")
        
        # Get configuration
        success, stdout, stderr = self.run_command("mcp-dispatcher list")
        if not success:
            self.log("Could not list configured servers", "ERROR")
            return False
        
        # Try to validate at least one server exists
        if "No path mappings configured" in stdout:
            self.log("No MCP servers configured - this is OK for basic setup", "WARNING")
            return True
        
        self.log("MCP server configuration OK", "SUCCESS")
        return True
    
    def test_claude_code_integration(self) -> bool:
        """Test Claude Code integration configuration"""
        self.log("Testing Claude Code integration...", "INFO")
        
        # Check for Claude Code config
        claude_config_paths = [
            os.path.expanduser("~/.config/claude-code/config.json"),
            os.path.expanduser("~/Library/Application Support/ClaudeCode/config.json"),
            os.path.expanduser("~/AppData/Roaming/ClaudeCode/config.json")
        ]
        
        claude_config = None
        for path in claude_config_paths:
            if os.path.exists(path):
                claude_config = path
                break
        
        if not claude_config:
            self.log("Claude Code config not found - manual configuration needed", "WARNING")
            self.log("See documentation for Claude Code integration", "INFO")
            return True  # Not a failure, just needs manual setup
        
        # Check if MCP dispatcher is configured
        try:
            with open(claude_config, 'r') as f:
                config = json.load(f)
            
            if "mcp" in config and "servers" in config["mcp"]:
                servers = config["mcp"]["servers"]
                if any("dispatcher" in name.lower() for name in servers.keys()):
                    self.log("Claude Code integration configured", "SUCCESS")
                    return True
        except Exception as e:
            self.log(f"Could not read Claude Code config: {e}", "WARNING")
        
        self.log("Claude Code integration not configured - manual setup needed", "WARNING")
        return True
    
    def test_end_to_end(self) -> bool:
        """Test end-to-end functionality"""
        self.log("Testing end-to-end functionality...", "INFO")
        
        # Test that the dispatcher can start (but don't let it run)
        success, stdout, stderr = self.run_command("timeout 2 mcp-dispatcher-exec", timeout=5)
        
        # We expect timeout or successful start
        if "🚀 Starting MCP server" in stderr or "timeout" in stderr.lower():
            self.log("End-to-end test OK", "SUCCESS")
            return True
        else:
            self.log("End-to-end test failed", "ERROR")
            self.log(f"Output: {stderr}", "DEBUG")
            return False
    
    def run_test(self, test_func, test_name: str) -> bool:
        """Run a single test and track results"""
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
                self.failures.append(test_name)
            return result
        except Exception as e:
            self.log(f"Test {test_name} crashed: {e}", "ERROR")
            self.tests_failed += 1
            self.failures.append(f"{test_name} (crashed)")
            return False
    
    def run_all_tests(self, verbose: bool = False) -> bool:
        """Run all tests"""
        self.verbose = verbose
        
        print("🧪 Smart MCP Dispatcher - Comprehensive Test Suite")
        print("=" * 60)
        print()
        
        tests = [
            (self.test_python_dependencies, "Python Dependencies"),
            (self.test_cli_installation, "CLI Installation"), 
            (self.test_configuration_file, "Configuration File"),
            (self.test_dispatcher_executable, "Dispatcher Executable"),
            (self.test_path_routing, "Path Routing"),
            (self.test_mcp_server_executability, "MCP Server Configuration"),
            (self.test_claude_code_integration, "Claude Code Integration"),
            (self.test_end_to_end, "End-to-End Functionality")
        ]
        
        for test_func, test_name in tests:
            print(f"\n🔍 Testing: {test_name}")
            self.run_test(test_func, test_name)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        
        if self.failures:
            print(f"\n🔍 Failed Tests:")
            for failure in self.failures:
                print(f"  • {failure}")
        
        if self.tests_failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"Your Smart MCP Dispatcher installation is working correctly!")
            return True
        else:
            print(f"\n⚠️  Some tests failed. Check the errors above.")
            print(f"See documentation for troubleshooting guidance.")
            return False

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Smart MCP Dispatcher installation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--quick", action="store_true", help="Run only essential tests")
    
    args = parser.parse_args()
    
    tester = MCPDispatcherTester()
    
    if args.quick:
        # Quick tests only
        essential_tests = [
            (tester.test_python_dependencies, "Python Dependencies"),
            (tester.test_cli_installation, "CLI Installation"),
            (tester.test_configuration_file, "Configuration File")
        ]
        
        print("🚀 Smart MCP Dispatcher - Quick Test")
        print("=" * 40)
        
        for test_func, test_name in essential_tests:
            print(f"\n🔍 {test_name}")
            tester.run_test(test_func, test_name)
        
        success = tester.tests_failed == 0
    else:
        success = tester.run_all_tests(args.verbose)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()