#!/usr/bin/env python3
"""
MCP Proxy Server - A proper MCP server that forwards requests to the selected backend server
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence
import subprocess

# Import MCP types and utilities
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    from mcp.types import (
        Tool, 
        TextContent, 
        ImageContent, 
        EmbeddedResource,
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListPromptsRequest,
        GetPromptRequest,
        PromptMessage,
        Prompt
    )
except ImportError:
    print("MCP library not found. Please install with: pip install mcp")
    sys.exit(1)

from mcp_dispatcher import MCPDispatcher

class MCPProxyServer:
    def __init__(self):
        self.dispatcher = MCPDispatcher()
        self.logger = logging.getLogger('mcp_proxy_server')
        self.server = Server("smart-mcp-dispatcher")
        self.current_backend_session: Optional[ClientSession] = None
        self.current_backend_config: Optional[Dict] = None
        
        # Set up handlers
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        self.server.list_prompts = self.list_prompts
        self.server.get_prompt = self.get_prompt
        
    async def get_backend_session(self) -> ClientSession:
        """Get or create backend MCP session for current directory"""
        current_path = os.environ.get('PWD', os.getcwd())
        server_config = self.dispatcher.find_matching_server(current_path)
        
        # If we already have a session for this server, reuse it
        if (self.current_backend_session and 
            self.current_backend_config == server_config):
            return self.current_backend_session
        
        # Close existing session if any
        if self.current_backend_session:
            try:
                await self.current_backend_session.__aexit__(None, None, None)
            except:
                pass
        
        # Create new session
        self.logger.info(f"Starting backend MCP server: {server_config['name']}")
        
        try:
            # Prepare environment variables
            env = os.environ.copy()
            if 'env' in server_config:
                env.update(server_config['env'])
            
            # Create server parameters
            server_params = StdioServerParameters(
                command=server_config['command'],
                args=server_config['args'],
                env=env
            )
            
            # Create session using context manager properly
            session_context = stdio_client(server_params)
            self.current_backend_session = await session_context.__aenter__()
            self.current_backend_config = server_config
            
            return self.current_backend_session
            
        except Exception as e:
            self.logger.error(f"Failed to start backend MCP server: {e}")
            raise
    
    async def list_tools(self) -> List[Tool]:
        """Forward list_tools request to backend server"""
        try:
            backend = await self.get_backend_session()
            result = await backend.list_tools()
            self.logger.info(f"Backend server provided {len(result.tools)} tools")
            return result.tools
        except Exception as e:
            self.logger.error(f"Error listing tools: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Forward call_tool request to backend server"""
        try:
            backend = await self.get_backend_session()
            result = await backend.call_tool(name, arguments)
            return result.content
        except Exception as e:
            self.logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error calling tool {name}: {str(e)}")]
    
    async def list_prompts(self) -> List[Prompt]:
        """Forward list_prompts request to backend server"""
        try:
            backend = await self.get_backend_session()
            result = await backend.list_prompts()
            self.logger.info(f"Backend server provided {len(result.prompts)} prompts")
            return result.prompts
        except Exception as e:
            self.logger.error(f"Error listing prompts: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, str] = None) -> PromptMessage:
        """Forward get_prompt request to backend server"""
        try:
            backend = await self.get_backend_session()
            result = await backend.get_prompt(name, arguments or {})
            return result
        except Exception as e:
            self.logger.error(f"Error getting prompt {name}: {e}")
            return PromptMessage(
                role="user",
                content=TextContent(type="text", text=f"Error getting prompt {name}: {str(e)}")
            )

async def main():
    """Main function to run the MCP proxy server"""
    proxy = MCPProxyServer()
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    proxy.logger.info("MCP Proxy Server starting...")
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await proxy.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="smart-mcp-dispatcher",
                server_version="1.0.0",
                capabilities=proxy.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())