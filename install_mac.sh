#!/bin/bash
# Smart MCP Dispatcher Installation Script for macOS
# This script installs the MCP dispatcher tools system-wide

echo "Smart MCP Dispatcher - macOS Installation"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7+ using:"
    echo "  brew install python"
    echo "  or download from https://python.org"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt || {
    echo "❌ Error: Failed to install Python dependencies"
    exit 1
}

# Create local bin directory
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

# Copy Python scripts
echo "📋 Installing MCP dispatcher scripts..."
cp mcp_dispatcher.py "$LOCAL_BIN/"
cp mcp_proxy.py "$LOCAL_BIN/"

# Create executable wrappers
cat > "$LOCAL_BIN/mcp-dispatcher" << 'EOF'
#!/bin/bash
python3 "$HOME/.local/bin/mcp_dispatcher.py" "$@"
EOF

cat > "$LOCAL_BIN/mcp-proxy" << 'EOF'
#!/bin/bash
python3 "$HOME/.local/bin/mcp_proxy.py" "$@"
EOF

# Make scripts executable
chmod +x "$LOCAL_BIN/mcp-dispatcher"
chmod +x "$LOCAL_BIN/mcp-proxy"
chmod +x "$LOCAL_BIN/mcp_dispatcher.py"
chmod +x "$LOCAL_BIN/mcp_proxy.py"

# Check if ~/.local/bin is in PATH and add if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️  Adding ~/.local/bin to PATH..."
    
    # Determine shell profile file
    if [[ "$SHELL" == */zsh ]]; then
        PROFILE_FILE="$HOME/.zshrc"
    elif [[ "$SHELL" == */bash ]]; then
        PROFILE_FILE="$HOME/.bash_profile"
        # Also check .bashrc for some systems
        if [[ -f "$HOME/.bashrc" && ! -f "$HOME/.bash_profile" ]]; then
            PROFILE_FILE="$HOME/.bashrc"
        fi
    else
        PROFILE_FILE="$HOME/.profile"
    fi
    
    # Add to PATH in profile
    echo "" >> "$PROFILE_FILE"
    echo "# Added by MCP Dispatcher installer" >> "$PROFILE_FILE"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$PROFILE_FILE"
    
    echo "✅ Added ~/.local/bin to PATH in $PROFILE_FILE"
    echo "🔄 Please restart your terminal or run: source $PROFILE_FILE"
else
    echo "✅ ~/.local/bin is already in PATH"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Restart your terminal or run: source ~/.$(basename $SHELL)rc"
echo "2. Run: ./setup.py (to configure your MCP servers)"
echo "3. Test: mcp-dispatcher test"
echo "4. Configure Claude Code with the proxy"
echo ""