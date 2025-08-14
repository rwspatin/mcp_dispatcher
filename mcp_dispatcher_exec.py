#!/usr/bin/env python3
"""
MCP Dispatcher Exec - Direct execution wrapper for Claude Code
This script determines which MCP server to run based on current directory
and then directly executes it (replacing the current process)
"""

import os
import sys
import subprocess
from mcp_dispatcher import MCPDispatcher

def main():
    """Main function to determine and execute the appropriate MCP server"""
    try:
        # Initialize dispatcher
        dispatcher = MCPDispatcher()
        
        # Get the appropriate server for current directory
        server_config = dispatcher.find_matching_server()
        
        # Prepare command
        cmd = [server_config['command']] + server_config['args']
        
        # Prepare environment
        env = os.environ.copy()
        if 'env' in server_config:
            env.update(server_config['env'])
        
        # Log which server we're starting
        dispatcher.logger.info(f"Executing MCP server: {server_config['name']}")
        dispatcher.logger.info(f"Command: {' '.join(cmd)}")
        
        # Replace current process with the MCP server
        # This ensures Claude Code gets direct access to the MCP server
        os.execvpe(cmd[0], cmd, env)
        
    except Exception as e:
        print(f"Error starting MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()