# Smart MCP Dispatcher - Claude Context

## Project Overview

The Smart MCP Dispatcher is a path-based routing system for MCP (Model Context Protocol) servers. It automatically selects which MCP server to use based on your current directory path, allowing developers to work with different MCP tools for different projects seamlessly.

## Key Features

- **Path-based routing**: Automatically selects MCP servers based on directory patterns
- **Multi-language support**: Works with Python, Node.js, Go, and any executable MCP servers
- **Wildcard support**: Uses glob patterns to match directory structures
- **CLI management**: Easy command-line interface for managing mappings
- **Transparent proxy**: Works seamlessly with Claude Code and other MCP clients
- **Default fallback**: Configurable default server when no patterns match
- **Local configuration**: Supports local `config.json` for project-specific setups
- **Configuration validation**: Validates setup and provides helpful error messages

## Architecture

### Core Components

1. **mcp_dispatcher.py** - Main dispatcher logic and CLI interface
2. **mcp_proxy.py** - MCP protocol proxy server that forwards requests
3. **setup.py** - Interactive configuration setup script
4. **config.json.template** - Template for user configuration
5. **install.sh** - System installation script

### How It Works

1. **Path Detection**: When Claude Code starts, the proxy detects your current working directory
2. **Pattern Mapping**: The dispatcher checks configured patterns against the current path using Python's `fnmatch`
3. **Server Selection**: The first matching pattern determines which MCP server to use
4. **Transparent Proxy**: All MCP requests are forwarded to the selected server
5. **Automatic Switching**: If you change directories, the proxy automatically switches servers

## File Structure

```
mcp-hadler/
├── mcp_dispatcher.py          # Main dispatcher logic
├── mcp_proxy.py               # MCP protocol proxy
├── setup.py                   # Interactive setup script
├── install.sh                 # System installation
├── config.json.template       # Configuration template
├── claude_config_example.json # Claude Code configuration example
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore patterns
├── README.md                  # Documentation
└── CLAUDE.md                  # This file
```

## Configuration System

### No Default Configuration
- The system **requires** user configuration - no hardcoded defaults
- Users must create their own `config.json` from the template
- Validation ensures proper configuration before starting

### Configuration Locations
1. **Local**: `config.json` (project-specific, preferred)
2. **Global**: `~/.mcp_dispatcher_config.json` (user-wide fallback)

### Configuration Structure
```json
{
  "path_mappings": [
    {
      "path_pattern": "/path/to/your/projects*",
      "mcp_server": {
        "name": "server-name",
        "command": "python|node|/path/to/binary",
        "args": ["server.py"],
        "description": "Server description"
      }
    }
  ],
  "default_mcp_server": {
    "name": "default-server",
    "command": "python",
    "args": ["/path/to/default/server.py"],
    "description": "Default server"
  },
  "logging": {
    "level": "INFO",
    "file": "/tmp/mcp_dispatcher.log"
  }
}
```

## Cross-Platform Support

The Smart MCP Dispatcher works on **Windows**, **macOS**, and **Linux** with platform-specific optimizations.

### Platform-Specific Features

#### Windows
- **Config location**: `%APPDATA%\mcp_dispatcher\config.json`
- **Installation**: `install.bat` - Installs to `%USERPROFILE%\Scripts`
- **Python command**: Usually `python`
- **Path examples**: `C:/Users/*/projects/web*`, `C:/projects/nodejs*`

#### macOS
- **Config location**: `~/Library/Application Support/mcp_dispatcher/config.json`
- **Installation**: `install_mac.sh` - Installs to `~/.local/bin`
- **Python command**: Usually `python3`
- **Path examples**: `/Users/*/projects/web*`, `/Users/*/Development/nodejs*`

#### Linux
- **Config location**: `~/.config/mcp_dispatcher/config.json`
- **Installation**: `install.sh` - Installs to `~/.local/bin`
- **Python command**: Usually `python3`
- **Path examples**: `/home/*/projects/web*`, `/home/*/development/nodejs*`

### Cross-Platform Path Handling

- **Pattern matching**: Always use forward slashes (`/`) in patterns, even on Windows
- **Path normalization**: The dispatcher automatically converts paths for proper matching
- **Wildcards**: Standard glob patterns work on all platforms

## Installation Process

### For Windows Users

1. **Clone repository**
   ```cmd
   git clone <repository-url>
   cd mcp-hadler
   ```

2. **Run interactive setup**
   ```cmd
   python setup.py
   ```

3. **Install system binaries**
   ```cmd
   install.bat
   ```

### For macOS Users

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd mcp-hadler
   ```

2. **Run interactive setup**
   ```bash
   ./setup.py
   ```

3. **Install system binaries**
   ```bash
   chmod +x install_mac.sh
   ./install_mac.sh
   ```

### For Linux Users

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd mcp-hadler
   ```

2. **Run interactive setup**
   ```bash
   ./setup.py
   ```

3. **Install system binaries**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Configure Claude Code (All Platforms)

Update Claude Code MCP configuration:
```json
{
  "mcp": {
    "servers": {
      "smart-dispatcher": {
        "command": "mcp-proxy",
        "args": []
      }
    }
  }
}
```

## CLI Commands

### Management Commands
- `mcp-dispatcher list` - Show all configured mappings
- `mcp-dispatcher add <pattern> <name> <command> <args...>` - Add new mapping
- `mcp-dispatcher remove <pattern>` - Remove mapping
- `mcp-dispatcher test [--path <path>]` - Test which server would be selected
- `mcp-dispatcher start [--path <path>]` - Start appropriate MCP server

### Examples
```bash
# Add a Python MCP server for web projects
mcp-dispatcher add "/home/*/projects/web*" \
    "web-mcp" \
    "python" \
    "/path/to/web-mcp/server.py" \
    --description "Web Development MCP"

# Add a Node.js MCP server  
mcp-dispatcher add "/home/*/projects/node*" \
    "node-mcp" \
    "node" \
    "/path/to/node-mcp/server.js" \
    --description "Node.js MCP"

# Test current directory
mcp-dispatcher test

# Test specific path
mcp-dispatcher test --path /home/user/projects/web-app
```

## Supported MCP Server Types

### Python MCP Servers
```json
{
  "command": "python",
  "args": ["/path/to/server.py"]
}
```

### Node.js MCP Servers
```json
{
  "command": "node", 
  "args": ["/path/to/server.js"]
}
```

### Compiled Binaries
```json
{
  "command": "/path/to/mcp-binary",
  "args": []
}
```

### Shell Scripts
```json
{
  "command": "/path/to/start-mcp.sh",
  "args": []
}
```

## Pattern Matching

Uses Python's `fnmatch` module:
- `*` - matches any number of characters
- `?` - matches any single character  
- `[seq]` - matches any character in seq
- `[!seq]` - matches any character not in seq

### Cross-Platform Pattern Examples

**Windows:**
```bash
"C:/Users/*/projects/my-app"           # Exact match
"C:/Users/*/projects/web*"             # Any user, web projects  
"C:/projects/{web,api}/*"              # Multiple project types
"D:/development/*/frontend"            # All frontend subdirectories
```

**macOS:**
```bash
"/Users/*/projects/my-app"             # Exact match
"/Users/*/projects/web*"               # Any user, web projects
"/Users/*/projects/{web,api}/*"        # Multiple project types
"/Users/*/Development/*/frontend"      # All frontend subdirectories
```

**Linux:**
```bash
"/home/*/projects/my-app"              # Exact match
"/home/*/projects/web*"                # Any user, web projects
"/home/*/projects/{web,api}/*"         # Multiple project types
"/home/*/development/*/frontend"       # All frontend subdirectories
```

**Important**: Always use forward slashes (`/`) in patterns, even on Windows!

## Error Handling

### Missing Configuration
When `config.json` is missing, shows:
```
❌ Configuration file not found!
Expected location: config.json

🔧 To get started:
1. Run the setup script: ./setup.py
2. Or copy the template: cp config.json.template config.json
3. Edit config.json with your MCP server paths

📖 You must configure AT LEAST:
   - One path mapping for your projects
   - A default MCP server

📚 See README.md for configuration examples
```

### Invalid Configuration
Validates and reports specific issues:
- Missing required fields
- Invalid server configurations
- Empty path mappings
- Malformed JSON

## Common Use Cases

### Multi-Project Developer
```json
{
  "path_mappings": [
    {
      "path_pattern": "/home/*/projects/crypto*",
      "mcp_server": {
        "name": "crypto-mcp",
        "command": "python",
        "args": ["/home/user/mcp-servers/crypto/server.py"]
      }
    },
    {
      "path_pattern": "/home/*/projects/web*", 
      "mcp_server": {
        "name": "web-mcp",
        "command": "node",
        "args": ["/home/user/mcp-servers/web/server.js"]
      }
    }
  ],
  "default_mcp_server": {
    "name": "general-mcp",
    "command": "python",
    "args": ["/home/user/mcp-servers/general/server.py"]
  }
}
```

### Team Environment
- Each team member configures their own paths
- Shared `config.json.template` with team-specific examples
- Local `config.json` for personal customization

## Troubleshooting

### Common Issues

1. **Server not starting**
   - Check MCP server command and arguments
   - Verify file paths exist and are executable
   - Check permissions

2. **Pattern not matching**
   - Use `mcp-dispatcher test` to verify patterns
   - Check path format and wildcards
   - Ensure patterns use absolute paths

3. **Configuration errors**
   - Run `./setup.py` to recreate config
   - Validate JSON syntax
   - Check required fields are present

### Debug Mode
```bash
export MCP_DISPATCHER_LOG_LEVEL=DEBUG
mcp-dispatcher test
```

## Development Notes

### Code Structure
- **MCPDispatcher class**: Core routing logic
- **MCPProxy class**: MCP protocol implementation
- **Configuration validation**: Ensures proper setup
- **Error handling**: User-friendly messages

### Key Design Decisions
1. **No hardcoded defaults** - Forces proper user configuration
2. **Template-based setup** - Provides structure without assumptions
3. **Local config priority** - Project-specific configurations
4. **Comprehensive validation** - Prevents runtime errors
5. **Interactive setup** - Guides users through configuration

## Installation Helper for Claude

When users ask for help with installation and configuration, you can:

1. **Guide them through the setup process**
2. **Help configure specific MCP servers** (Python, Node.js, etc.)
3. **Create custom path patterns** for their project structure
4. **Troubleshoot configuration issues**
5. **Validate their setup** before they run it

### Quick Setup Commands for Users

**Windows:**
```cmd
REM 1. Initial setup
python setup.py

REM 2. Install system-wide
install.bat

REM 3. Test configuration  
mcp-dispatcher test

REM 4. List current setup
mcp-dispatcher list
```

**macOS/Linux:**
```bash
# 1. Initial setup
./setup.py

# 2. Install system-wide (choose correct script)
chmod +x install_mac.sh && ./install_mac.sh    # macOS
chmod +x install.sh && ./install.sh            # Linux

# 3. Test configuration  
mcp-dispatcher test

# 4. List current setup
mcp-dispatcher list
```

The project is designed to be completely generic and community-friendly, requiring users to configure their own paths and MCP servers while providing helpful guidance throughout the process.