#!/usr/bin/env python3
"""
MCP Proxy Server - Acts as a transparent proxy to route MCP requests to the appropriate server
based on the current directory path.

This proxy server implements the MCP protocol and forwards all requests to the selected
MCP server while maintaining full compatibility with Claude Code and other MCP clients.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional
import subprocess
from pathlib import Path

# Import MCP types and utilities
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
except ImportError:
    print("MCP library not found. Please install with: pip install mcp")
    sys.exit(1)

from mcp_dispatcher import MCPDispatcher

class MCPProxy:
    def __init__(self):
        self.dispatcher = MCPDispatcher()
        self.logger = logging.getLogger('mcp_proxy')
        self.current_session: Optional[ClientSession] = None
        self.current_process: Optional[subprocess.Popen] = None
        
    async def get_current_mcp_session(self) -> ClientSession:
        """Get or create MCP session for current directory"""
        current_path = os.getcwd()
        server_config = self.dispatcher.find_matching_server(current_path)
        
        # If we already have a session for this server, reuse it
        if (self.current_session and 
            hasattr(self.current_session, '_server_config') and 
            self.current_session._server_config == server_config):
            return self.current_session
        
        # Close existing session if any
        if self.current_session:
            await self.current_session.close()
        if self.current_process:
            self.current_process.terminate()
            await asyncio.sleep(0.1)
        
        # Start new MCP server process
        cmd = [server_config['command']] + server_config['args']
        self.logger.info(f"Starting MCP server: {' '.join(cmd)}")
        
        try:
            self.current_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Create new session
            server_params = StdioServerParameters(
                command=server_config['command'],
                args=server_config['args']
            )
            
            self.current_session = await stdio_client(server_params)
            self.current_session._server_config = server_config  # Store config for comparison
            
            return self.current_session
            
        except Exception as e:
            self.logger.error(f"Failed to start MCP server: {e}")
            raise

def create_proxy_server() -> Server:
    """Create the MCP proxy server"""
    server = Server("mcp-dispatcher-proxy")
    proxy = MCPProxy()
    
    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        """Proxy tool listing to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.list_tools()
            return result.tools
        except Exception as e:
            proxy.logger.error(f"Error listing tools: {e}")
            return []
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Proxy tool calls to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.call_tool(name, arguments)
            return result.content
        except Exception as e:
            proxy.logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    @server.list_resources()
    async def handle_list_resources():
        """Proxy resource listing to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.list_resources()
            return result.resources
        except Exception as e:
            proxy.logger.error(f"Error listing resources: {e}")
            return []
    
    @server.read_resource()
    async def handle_read_resource(uri: str):
        """Proxy resource reading to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.read_resource(uri)
            return result.contents
        except Exception as e:
            proxy.logger.error(f"Error reading resource {uri}: {e}")
            return []
    
    @server.list_prompts()
    async def handle_list_prompts():
        """Proxy prompt listing to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.list_prompts()
            return result.prompts
        except Exception as e:
            proxy.logger.error(f"Error listing prompts: {e}")
            return []
    
    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict):
        """Proxy prompt retrieval to current MCP server"""
        try:
            session = await proxy.get_current_mcp_session()
            result = await session.get_prompt(name, arguments)
            return result
        except Exception as e:
            proxy.logger.error(f"Error getting prompt {name}: {e}")
            return None
    
    return server

async def main():
    """Main entry point for the proxy server"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('mcp_proxy')
    
    # Create and run the proxy server
    server = create_proxy_server()
    
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-dispatcher-proxy",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())