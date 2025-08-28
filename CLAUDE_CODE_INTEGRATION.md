# Claude Code Integration

This document describes how the MCP dispatcher integrates with Claude Code and the fixes applied for proper path detection.

## The Problem

Claude Code sets the working directory via the `PWD` environment variable, but standard Python `os.getcwd()` returns the directory where the MCP process was started, not where Claude Code is actually working. This caused incorrect MCP server selection.

## The Solution

Both `mcp_proxy.py` and `mcp-dispatcher-exec` have been updated to use:

```python
current_path = os.environ.get('PWD', os.getcwd())
```

Instead of just:

```python
current_path = os.getcwd()
```

This ensures the dispatcher detects the correct working directory that Claude Code is using.

## Configuration

### Global Configuration

The dispatcher works globally with Claude Code configuration:

**~/.config/claude-code/config.json:**
```json
{
  "mcp": {
    "servers": {
      "smart-mcp-dispatcher": {
        "command": "/path/to/mcp-proxy",
        "args": [],
        "env": {
          "MCP_DISPATCHER_CONFIG": "/path/to/your/dispatcher/config.json",
          "YOUR_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

### Path Mapping Example

**config.json:**
```json
{
  "path_mappings": [
    {
      "path_pattern": "/path/to/crypto/projects*",
      "mcp_server": {
        "name": "crypto-mcp",
        "command": "npx",
        "args": ["tsx", "/path/to/crypto-mcp/src/index.ts"]
      }
    },
    {
      "path_pattern": "/path/to/other/projects*",
      "mcp_server": {
        "name": "other-mcp",
        "command": "python3",
        "args": ["/path/to/other-mcp/server.py"]
      }
    }
  ],
  "default_mcp_server": {
    "name": "default-mcp",
    "command": "python3",
    "args": ["/path/to/default/server.py"]
  }
}
```

## Benefits

- **No local .mcp.json files needed** in project directories
- **Automatic path-based routing** based on Claude Code's current directory
- **Global configuration** - install once, works everywhere
- **Community-friendly** - generic configuration without hardcoded paths

## Testing

Test the dispatcher selection:

```bash
# Test what server would be selected for current directory
mcp-dispatcher test

# Test what server would be selected for specific path
mcp-dispatcher test --path /path/to/your/project
```