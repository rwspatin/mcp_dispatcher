#!/bin/bash
# Smart MCP Dispatcher Installation Script for Linux
# This script installs the MCP dispatcher tools system-wide

set -e

echo "Smart MCP Dispatcher - Linux Installation"
echo "=========================================="

# Get installation directory
INSTALL_DIR="${1:-$HOME/.local/bin}"
CONFIG_DIR="$HOME/.config/mcp-dispatcher"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"

# Copy scripts
echo "📂 Installing scripts to $INSTALL_DIR"
cp mcp_dispatcher.py "$INSTALL_DIR/"
cp mcp_proxy.py "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/mcp_dispatcher.py"
chmod +x "$INSTALL_DIR/mcp_proxy.py"

# Create symlinks for easier access
ln -sf "$INSTALL_DIR/mcp_dispatcher.py" "$INSTALL_DIR/mcp-dispatcher"
ln -sf "$INSTALL_DIR/mcp_proxy.py" "$INSTALL_DIR/mcp-proxy"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --user mcp

# Create default configuration
echo "⚙️  Creating default configuration..."
python3 "$INSTALL_DIR/mcp_dispatcher.py" list > /dev/null 2>&1 || true

# Add to PATH if not already there
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "📝 Adding $INSTALL_DIR to PATH..."
    echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$HOME/.bashrc"
    echo "Please run: source ~/.bashrc or restart your terminal"
fi

echo "✅ Installation complete!"
echo ""
echo "Usage examples:"
echo "  mcp-dispatcher list                    # List all path mappings"
echo "  mcp-dispatcher test                    # Test current directory"
echo "  mcp-dispatcher add PATTERN NAME CMD    # Add new mapping"
echo ""
echo "To use with Claude Code, create a .mcp.json file in your project root:"
echo "{"
echo "  \"mcpServers\": {"
echo "    \"smart-mcp-dispatcher\": {"
echo "      \"command\": \"$INSTALL_DIR/mcp-proxy\","
echo "      \"args\": [],"
echo "      \"env\": {"
echo "        \"MCP_DISPATCHER_CONFIG\": \"$(pwd)/config.json\""
echo "      }"
echo "    }"
echo "  }"
echo "}"
echo ""
echo "Configuration files:"
echo "  - MCP Dispatcher config: ~/.mcp_dispatcher_config.json or ./config.json"
echo "  - Claude Code config: .mcp.json (in project root)"