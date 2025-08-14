# Smart MCP Dispatcher

🚀 **Global MCP server that automatically selects the right MCP tools based on your current directory!**

Perfect for developers working on multiple projects that require different MCP tools and capabilities. Works globally in Claude Code - install once, use everywhere!

## ✨ Features

- **🗂️ Path-based routing**: Automatically selects MCP servers based on directory patterns
- **🌍 Global installation**: Works everywhere in Claude Code without project-specific setup
- **🔧 Multi-language support**: Works with Python, Node.js, and any executable MCP servers
- **🎯 Wildcard support**: Use glob patterns to match directory structures
- **⚡ CLI management**: Easy-to-use command-line interface for managing mappings
- **🔄 Transparent operation**: Works seamlessly with Claude Code and other MCP clients
- **🛡️ Default fallback**: Configurable default server when no patterns match
- **📁 Local configuration**: Supports local `config.json` for project-specific setups

## ⚡ Super Quick Start

### 🤖 Easiest Way (AI-Powered)
```bash
git clone <repository-url> && cd mcp_dispatcher && ./install_global.sh
claude chat "Set up MCP dispatcher with Zen MCP and popular servers for development"
```

### 🎯 Interactive Way (Guided)
```bash
git clone <repository-url> && cd mcp_dispatcher
./install_global.sh && ./setup_popular_servers.py
```

### 🛠️ Manual Way (Advanced)
```bash
git clone <repository-url> && cd mcp_dispatcher
./setup.py && ./install_global.sh && mcp-dispatcher test-install
```

## 🚀 Platform-Specific Installation

### 🐧 Linux
```bash
# 1. Clone repository
git clone <repository-url>
cd mcp_dispatcher

# 2. Choose your setup method:
# Option A: Let Claude configure everything
claude chat "Help me set up MCP dispatcher with recommended servers"

# Option B: Interactive setup
./install_global.sh && ./setup_popular_servers.py

# Option C: Manual setup
./setup.py && ./install_global.sh

# 3. Test installation
mcp-dispatcher test-install
```

### 🍎 macOS
```bash
# 1. Clone repository
git clone <repository-url>
cd mcp_dispatcher

# 2. Choose your setup method:
# Option A: Let Claude configure everything
claude chat "Help me set up MCP dispatcher with recommended servers"

# Option B: Interactive setup
./install_global.sh && ./setup_popular_servers.py

# Option C: Manual setup
./setup.py && ./install_global.sh

# 3. Test installation
mcp-dispatcher test-install
```

### 🪟 Windows
```cmd
REM 1. Clone repository
git clone <repository-url>
cd mcp_dispatcher

REM 2. Choose your setup method:
REM Option A: Let Claude configure everything
claude chat "Help me set up MCP dispatcher with recommended servers"

REM Option B: Interactive setup
install_global.bat && python setup_popular_servers.py

REM Option C: Manual setup
python setup.py && install_global.bat

REM 3. Test installation
mcp-dispatcher test-install
```

## Installation

### Windows

1. Clone or download this repository
2. Run the setup script to configure your MCP servers:
   ```cmd
   python setup.py
   ```
3. Run the installation script:
   ```cmd
   install.bat
   ```
4. Add `%USERPROFILE%\Scripts` to your PATH if not already there

### macOS

1. Clone or download this repository
2. Run the setup script to configure your MCP servers:
   ```bash
   ./setup.py
   ```
3. Run the installation script:
   ```bash
   chmod +x install_mac.sh
   ./install_mac.sh
   ```
4. Restart your terminal or run `source ~/.zshrc`

### Linux

1. Clone or download this repository
2. Run the setup script to configure your MCP servers:
   ```bash
   ./setup.py
   ```
3. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
4. Restart your terminal or run `source ~/.bashrc`

## Quick Start

### 1. Initial Setup

The setup script will guide you through configuration:

```bash
./setup.py
```

This will:
- Create your `config.json` from the template
- Ask for your default MCP server
- Set up your first project path mapping  
- Validate the configuration

### 2. Add More Mappings (Optional)

After setup, add more mappings for different project types:

```bash
# Example: Add mapping for web development projects
mcp-dispatcher add "/home/*/projects/web-dev*" \
    "web-dev-mcp" \
    "python" \
    "/path/to/your/web-dev-mcp/server.py" \
    --description "Web Development MCP Server"

# Example: Add mapping for Node.js projects
mcp-dispatcher add "/home/*/projects/nodejs*" \
    "nodejs-mcp" \
    "node" \
    "/path/to/your/nodejs-mcp/server.js" \
    --description "Node.js MCP Server"
```

### 3. Test Your Configuration

```bash
# Test current directory
mcp-dispatcher test

# Test specific path
mcp-dispatcher test --path /path/to/your/project
```

### 4. Configure Claude Code (Global)

The dispatcher works globally in Claude Code. Choose one method:

#### Option A: Claude Code CLI (Recommended)
```bash
claude mcp add smart-mcp-dispatcher --scope user /path/to/mcp-dispatcher-exec
```

#### Option B: Manual Configuration
Edit your Claude Code config file:

**File locations:**
- Linux: `~/.config/claude-code/config.json`
- macOS: `~/Library/Application Support/ClaudeCode/config.json`  
- Windows: `%APPDATA%\ClaudeCode\config.json`

```json
{
  "mcp": {
    "servers": {
      "smart-mcp-dispatcher": {
        "command": "/path/to/mcp-dispatcher-exec",
        "args": [],
        "env": {
          "MCP_DISPATCHER_CONFIG": "/path/to/your/config.json"
        }
      }
    }
  }
}
```

**That's it!** No need for `.mcp.json` files in every project. The dispatcher now works globally across all directories.

## 🌟 Recommended MCP Servers

Get started quickly with these popular, community-tested MCP servers:

### 🧠 **Zen MCP Server** (Recommended for Beginners)
**Multi-AI orchestration with guided workflows**
- **What it does**: Provides access to multiple AI models (Gemini, OpenAI, O3) through Claude Code
- **Best for**: Developers who want enhanced AI assistance with code analysis, debugging, and collaboration
- **Installation**: `npx zen-mcp-server-199bio` or clone from [BeehiveInnovations/zen-mcp-server](https://github.com/BeehiveInnovations/zen-mcp-server)
- **Setup**: Requires API keys (GEMINI_API_KEY, OPENAI_API_KEY, etc.)

### 💻 **Filesystem MCP** (Essential)
**File and directory operations**
- **What it does**: Read, write, search files and directories through Claude Code
- **Best for**: Essential for any development work
- **Installation**: Built into Claude Code - just enable it
- **Setup**: No additional configuration needed

### 🌐 **Browser MCP** (Web Development)
**Web page interaction and automation**
- **What it does**: Navigate websites, extract content, interact with web pages
- **Best for**: Web scraping, testing, content analysis
- **Installation**: `npx @modelcontextprotocol/server-browser`
- **Setup**: May require browser configuration

### 🛠️ **Git MCP** (Development)
**Git repository operations**
- **What it does**: Git commands, repository analysis, commit management
- **Best for**: Code version control and repository analysis
- **Installation**: `npx @modelcontextprotocol/server-git`
- **Setup**: Requires git installation

### 📊 **SQLite MCP** (Data Analysis)
**Database operations**
- **What it does**: Query and analyze SQLite databases
- **Best for**: Data analysis, database management
- **Installation**: `npx @modelcontextprotocol/server-sqlite`
- **Setup**: Requires SQLite installation

## 🚀 Quick Setup Options

### Option A: Claude AI Assistant (Easiest)
Let Claude Code CLI set everything up automatically:

```bash
# 1. Install Smart MCP Dispatcher
git clone <repository-url> && cd mcp_dispatcher && ./install_global.sh

# 2. Ask Claude to configure everything for you
claude chat "Please help me set up the Smart MCP Dispatcher with Zen MCP server as default and filesystem MCP for development. Configure the path mappings for my projects."
```

**Claude will automatically:**
- ✅ Install recommended MCP servers
- ✅ Configure API keys securely
- ✅ Set up path mappings for your projects
- ✅ Test the entire installation
- ✅ Provide usage guidance

### Option B: Interactive Setup (Recommended)
Use our guided setup script for popular servers:

```bash
# 1. Install Smart MCP Dispatcher
git clone <repository-url> && cd mcp_dispatcher && ./install_global.sh

# 2. Run the interactive setup for popular servers
./setup_popular_servers.py

# 3. Test your installation
mcp-dispatcher test-install
```

**Available servers:**
- 🧠 **Zen MCP** - Multi-AI orchestration (default recommendation)
- 💻 **Filesystem MCP** - Essential file operations
- 🛠️ **Git MCP** - Repository management
- 🌐 **Browser MCP** - Web automation
- 📊 **SQLite MCP** - Database operations

### Option C: Manual Setup (Advanced Users)
Configure everything yourself with full control:

```bash
# 1. Install Smart MCP Dispatcher
git clone <repository-url> && cd mcp_dispatcher && ./setup.py && ./install_global.sh

# 2. Install your chosen MCP servers manually
# 3. Configure path mappings with mcp-dispatcher add
# 4. Test with mcp-dispatcher test-install
```

## Usage Examples

### Directory Structure Example

```
/home/user/projects/
├── web-dev/ecommerce-site/                      # Uses web-dev-mcp
├── web-dev/portfolio/                           # Uses web-dev-mcp  
├── nodejs/api-server/                           # Uses nodejs-mcp (Node.js)
├── nodejs/frontend-app/                         # Uses nodejs-mcp (Node.js)
├── special-projects/data-pipeline/              # Uses special-mcp
└── other/random-project/                        # Uses default MCP server
```

### CLI Commands

```bash
# List all configured mappings
mcp-dispatcher list

# Add a new mapping
mcp-dispatcher add "/path/to/your/projects*" "custom-mcp" "python" "/path/to/server.py"

# Remove a mapping
mcp-dispatcher remove "/path/to/your/projects*"

# Test which server would be selected
mcp-dispatcher test
mcp-dispatcher test --path /specific/path

# Start MCP server directly (for testing)
mcp-dispatcher start
mcp-dispatcher start --path /specific/path
```

## Configuration

**IMPORTANT**: You must create your own `config.json` file. The dispatcher will not work without proper configuration.

### Setup Process

1. **Run setup script**: `./setup.py` - Interactive configuration
2. **Manual setup**: Copy `config.json.template` to `config.json` and edit
3. **Validation**: The dispatcher validates your config on startup

### Configuration File

The configuration is stored in `config.json` (local) or `~/.mcp_dispatcher_config.json` (global):

```json
{
  "path_mappings": [
    {
      "path_pattern": "/path/to/your/project-type-a*",
      "mcp_server": {
        "name": "project-a-mcp",
        "command": "python",
        "args": ["/path/to/your/project-a-mcp/server.py"],
        "description": "Custom MCP Server for Project Type A"
      }
    },
    {
      "path_pattern": "/path/to/your/project-type-b*",
      "mcp_server": {
        "name": "project-b-mcp",
        "command": "node",
        "args": ["/path/to/your/project-b-mcp/server.js"],
        "description": "Custom Node.js MCP Server for Project Type B"
      }
    }
  ],
  "default_mcp_server": {
    "name": "default-mcp",
    "command": "python", 
    "args": ["/path/to/your/default-mcp/server.py"],
    "description": "Default MCP Server"
  }
}
```

## Pattern Matching

The dispatcher uses Python's `fnmatch` for pattern matching, which supports:

- `*` - matches any number of characters
- `?` - matches any single character  
- `[seq]` - matches any character in seq
- `[!seq]` - matches any character not in seq

### Pattern Examples

```bash
# Match specific directory
"/home/user/projects/my-app"

# Match any user's project directory
"/home/*/projects/my-app"

# Match any subdirectory under a project type
"/home/*/projects/web-dev*" 

# Match multiple project types
"/home/*/projects/{frontend,backend}/*"
```

## How It Works

1. **Path Detection**: When Claude Code starts, the proxy detects your current working directory
2. **Pattern Matching**: The dispatcher checks configured patterns against the current path
3. **Server Selection**: The first matching pattern determines which MCP server to use
4. **Transparent Proxy**: All MCP requests are forwarded to the selected server
5. **Automatic Switching**: If you change directories, the proxy automatically switches servers

## Advanced Usage

### Environment-Specific Configurations

You can create different configurations for different environments:

```bash
# Development configuration
mcp-dispatcher --config ~/.mcp_dispatcher_dev.json list

# Production configuration  
mcp-dispatcher --config ~/.mcp_dispatcher_prod.json list
```

### Debugging

Enable debug logging to troubleshoot path matching:

```bash
export MCP_DISPATCHER_LOG_LEVEL=DEBUG
mcp-dispatcher test
```

### Integration with IDE

Most IDEs respect the current working directory when running commands. The dispatcher will automatically use the appropriate MCP server based on your project context.

## Supported MCP Server Types

The dispatcher supports any MCP server implementation:

### Python MCP Servers
```bash
mcp-dispatcher add "/path/to/your/python-projects*" \
    "my-python-mcp" \
    "python" \
    "/path/to/your/python-mcp/server.py"
```

### Node.js MCP Servers
```bash
mcp-dispatcher add "/path/to/your/node-projects*" \
    "my-node-mcp" \
    "node" \
    "/path/to/your/node-mcp/server.js"

# Or compiled TypeScript
mcp-dispatcher add "/path/to/your/typescript-projects*" \
    "my-ts-mcp" \
    "node" \
    "/path/to/your/ts-mcp/build/index.js"
```

### Other Executable MCP Servers
```bash
# Go binary
mcp-dispatcher add "/path/to/your/go-projects*" \
    "my-go-mcp" \
    "/path/to/your/go-mcp-binary"

# Shell script wrapper
mcp-dispatcher add "/path/to/your/custom-projects*" \
    "my-custom-mcp" \
    "/path/to/your/start-mcp.sh"
```

## Troubleshooting

### Common Issues

1. **Path not matching**: Use `mcp-dispatcher test` to verify pattern matching
2. **Server not starting**: Check that the MCP server command and arguments are correct
3. **Permissions**: Ensure scripts are executable and in your PATH

### Debug Mode

Run with debug logging:

```bash
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from mcp_dispatcher import MCPDispatcher
d = MCPDispatcher()
d.test_current_path()
"
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details.