#!/usr/bin/env python3
"""
Setup script to configure the Smart MCP Dispatcher for your specific environment.
"""

import os
import json
from pathlib import Path
from mcp_dispatcher import MCPDispatcher

def setup_dispatcher():
    """Interactive setup for the MCP Dispatcher"""
    print("🚀 Smart MCP Dispatcher Setup")
    print("=" * 40)
    
    dispatcher = MCPDispatcher()
    
    # Clear existing configuration for fresh setup
    dispatcher.config = {
        "path_mappings": [],
        "default_mcp_server": {},
        "logging": {
            "level": "INFO",
            "file": "/tmp/mcp_dispatcher.log"
        }
    }
    
    print("\n1. Setting up Transfero Crypto MCP Server...")
    transfero_crypto_path = "/home/rwspatin/git/transfero/transferoswiss/crypto/crypto-mcp/server.py"
    if os.path.exists(os.path.dirname(transfero_crypto_path)):
        print(f"   ✓ Transfero crypto directory found")
        dispatcher.add_path_mapping(
            "/home/*/git/transfero/transferoswiss/crypto*",
            "transfero-crypto-mcp",
            "python",
            [transfero_crypto_path],
            "Transfero Crypto MCP Server"
        )
        print(f"   ✓ Added mapping for Transfero crypto projects")
    else:
        print(f"   ⚠ Transfero crypto directory not found at expected location")
        print(f"     You can add it later when you create the MCP server")
    
    print("\n2. Setting up DataVenia MCP Server...")
    datavenia_path = input("   Enter path to DataVenia MCP server (or press Enter to skip): ").strip()
    if datavenia_path and os.path.exists(datavenia_path):
        dispatcher.add_path_mapping(
            "/home/*/git/*/datavenia*",
            "datavenia-mcp", 
            "python",
            [datavenia_path],
            "DataVenia MCP Server"
        )
        print(f"   ✓ Added mapping for DataVenia projects")
    else:
        # Add placeholder mapping
        dispatcher.add_path_mapping(
            "/home/*/git/*/datavenia*",
            "datavenia-mcp",
            "python", 
            ["/path/to/datavenia-mcp/server.py"],
            "DataVenia MCP Server (UPDATE PATH)"
        )
        print(f"   ⚠ Added placeholder mapping - update the path later")
    
    print("\n3. Setting up Zen MCP Server...")
    zen_path = "/home/rwspatin/git/ia/zen-mcp-server/server.py"
    if os.path.exists(zen_path):
        print(f"   ✓ Zen MCP server found")
        dispatcher.add_path_mapping(
            "/home/*/git/ia/zen-mcp-server*",
            "zen-mcp",
            "python",
            [zen_path],
            "Zen MCP Server"
        )
        
        # Set as default
        dispatcher.config["default_mcp_server"] = {
            "name": "zen-mcp",
            "command": "python",
            "args": [zen_path],
            "description": "Default Zen MCP Server"
        }
        print(f"   ✓ Set Zen MCP as default server")
    else:
        print(f"   ⚠ Zen MCP server not found at {zen_path}")
        print(f"     Using basic fallback configuration")
        dispatcher.config["default_mcp_server"] = {
            "name": "basic-mcp",
            "command": "echo",
            "args": ["No MCP server configured"],
            "description": "Placeholder - configure your default MCP server"
        }
    
    # Save configuration
    dispatcher._save_config()
    
    print(f"\n✅ Configuration saved to {dispatcher.config_file}")
    print("\n📋 Summary:")
    dispatcher.list_mappings()
    
    print(f"\n🔧 Next Steps:")
    print(f"1. Update your Claude Code configuration to use the dispatcher:")
    print(f'   Add this to your MCP configuration:')
    print(f'   {{')
    print(f'     "mcp": {{')
    print(f'       "servers": {{')
    print(f'         "smart-dispatcher": {{')
    print(f'           "command": "{os.path.abspath("mcp_proxy.py")}",')
    print(f'           "args": []')
    print(f'         }}')
    print(f'       }}')
    print(f'     }}')
    print(f'   }}')
    print(f"")
    print(f"2. Create your crypto MCP server in:")
    print(f"   /home/rwspatin/git/transfero/transferoswiss/crypto/crypto-mcp/")
    print(f"")
    print(f"3. Test the dispatcher:")
    print(f"   python3 mcp_dispatcher.py test")
    print(f"   python3 mcp_dispatcher.py test --path /home/rwspatin/git/transfero/transferoswiss/crypto/test")

if __name__ == "__main__":
    setup_dispatcher()