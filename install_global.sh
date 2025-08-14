#!/bin/bash
#
# Smart MCP Dispatcher - Global Installation Script
# This script installs the MCP dispatcher globally for Claude Code
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Platform detection
PLATFORM=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="windows"
else
    echo -e "${RED}❌ Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Smart MCP Dispatcher - Global Installation${NC}"
echo -e "${BLUE}Platform detected: $PLATFORM${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python 3 found${NC}"
fi

# Check Claude Code
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠️  Claude Code CLI not found in PATH${NC}"
    echo -e "${YELLOW}   Installation will continue, but you'll need to configure manually${NC}"
    CLAUDE_CLI_AVAILABLE=false
else
    echo -e "${GREEN}✅ Claude Code CLI found${NC}"
    CLAUDE_CLI_AVAILABLE=true
fi

echo ""

# Step 1: Run setup if config doesn't exist
echo -e "${YELLOW}📝 Step 1: Configuration Setup${NC}"
if [[ ! -f "config.json" ]]; then
    echo -e "${BLUE}Running interactive setup...${NC}"
    if [[ -x "./setup.py" ]]; then
        ./setup.py
    else
        python3 setup.py
    fi
else
    echo -e "${GREEN}✅ Configuration file already exists${NC}"
fi

# Step 2: Install binaries
echo -e "${YELLOW}🔧 Step 2: Installing Binaries${NC}"

if [[ "$PLATFORM" == "linux" ]]; then
    if [[ -x "./install.sh" ]]; then
        ./install.sh
    else
        chmod +x install.sh && ./install.sh
    fi
    BINARY_PATH="$HOME/.local/bin/mcp-dispatcher-exec"
    CONFIG_PATH="$HOME/.config/mcp_dispatcher/config.json"
elif [[ "$PLATFORM" == "macos" ]]; then
    if [[ -x "./install_mac.sh" ]]; then
        ./install_mac.sh
    else
        chmod +x install_mac.sh && ./install_mac.sh
    fi
    BINARY_PATH="$HOME/.local/bin/mcp-dispatcher-exec"
    CONFIG_PATH="$HOME/Library/Application Support/mcp_dispatcher/config.json"
else
    echo -e "${RED}❌ Windows installation not supported by this script${NC}"
    echo -e "${YELLOW}Please run install.bat manually${NC}"
    exit 1
fi

# Step 3: Configure Claude Code
echo -e "${YELLOW}⚙️  Step 3: Claude Code Configuration${NC}"

if [[ "$CLAUDE_CLI_AVAILABLE" == true ]]; then
    echo -e "${BLUE}Configuring Claude Code globally...${NC}"
    
    # Try to add the MCP server
    if claude mcp add smart-mcp-dispatcher --scope user "$BINARY_PATH" 2>/dev/null; then
        echo -e "${GREEN}✅ Claude Code configured successfully using CLI${NC}"
        CLAUDE_CONFIGURED=true
    else
        echo -e "${YELLOW}⚠️  Claude CLI configuration failed, will show manual instructions${NC}"
        CLAUDE_CONFIGURED=false
    fi
else
    CLAUDE_CONFIGURED=false
fi

# Step 4: Manual configuration instructions if needed
if [[ "$CLAUDE_CONFIGURED" == false ]]; then
    echo -e "${YELLOW}📖 Manual Configuration Required${NC}"
    echo ""
    echo -e "${BLUE}Please add the following to your Claude Code configuration:${NC}"
    echo ""
    
    if [[ "$PLATFORM" == "linux" ]]; then
        CLAUDE_CONFIG="$HOME/.config/claude-code/config.json"
    elif [[ "$PLATFORM" == "macos" ]]; then
        CLAUDE_CONFIG="$HOME/Library/Application Support/ClaudeCode/config.json"
    fi
    
    echo -e "${YELLOW}Configuration file location:${NC} $CLAUDE_CONFIG"
    echo ""
    echo -e "${YELLOW}Configuration to add:${NC}"
    cat << EOF
{
  "mcp": {
    "servers": {
      "smart-mcp-dispatcher": {
        "command": "$BINARY_PATH",
        "args": [],
        "env": {
          "MCP_DISPATCHER_CONFIG": "$(pwd)/config.json"
        }
      }
    }
  }
}
EOF
    echo ""
fi

# Step 5: Test installation
echo -e "${YELLOW}🧪 Step 5: Testing Installation${NC}"

if mcp-dispatcher test &>/dev/null; then
    echo -e "${GREEN}✅ MCP Dispatcher test successful${NC}"
else
    echo -e "${RED}❌ MCP Dispatcher test failed${NC}"
    echo -e "${YELLOW}Check your configuration and try: mcp-dispatcher test${NC}"
fi

# Step 6: Final instructions
echo ""
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo ""
echo -e "${BLUE}What's Next:${NC}"
echo -e "1. ${GREEN}Test different directories:${NC} cd to various project folders and run ${YELLOW}mcp-dispatcher test${NC}"
echo -e "2. ${GREEN}Add more mappings:${NC} Use ${YELLOW}mcp-dispatcher add${NC} to configure more project paths"
echo -e "3. ${GREEN}List current setup:${NC} Run ${YELLOW}mcp-dispatcher list${NC} to see all configured servers"

if [[ "$CLAUDE_CONFIGURED" == false ]]; then
    echo -e "4. ${YELLOW}Configure Claude Code:${NC} Follow the manual configuration instructions above"
    echo -e "5. ${GREEN}Restart Claude Code${NC} for changes to take effect"
else
    echo -e "4. ${GREEN}Restart Claude Code${NC} for changes to take effect"
fi

echo ""
echo -e "${BLUE}The Smart MCP Dispatcher is now installed globally!${NC}"
echo -e "${BLUE}It will automatically route to the correct MCP server based on your directory.${NC}"
echo ""