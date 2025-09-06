# Cloudera Hive MCP Server (via Impala)

This is a A Model Context Protocol server that provides read-only access to Hive tables via Apache Impala. This server enables LLMs to inspect database schemas and execute read-only queries.

- `execute_query(query: str)`: Run any SQL query on Impala and return the results as JSON.
- `show_tables()`: List all tables available in the current database.

## Usage with Claude Desktop/Cursor IDE

To use this server with the Claude Desktop app or Cursor IDE, add the following configuration to the "mcpServers" section of your `claude_desktop_config.json` or `mcp.json` config file under Cursor setting:

### Option 1: Direct installation from GitHub (Recommended)
```json
{
  "mcpServers": {
    "hive-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/dhirajkumarsinha27091982/hive-mcp-server@main",
        "run-server"
      ],
      "env": {
        "IMPALA_HOST": "coordinator-default-impala.example.com",
        "IMPALA_PORT": "21050",
        "IMPALA_USER": "username",
        "IMPALA_PASSWORD": "password",
        "IMPALA_DATABASE": "default"
      }
    }
  }
}
```

### Option 2: Local installation (after cloning the repository)
```json
{
  "mcpServers": {
    "hive-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/hive-mcp-server",
        "run",
        "src/hive_mcp_server/server.py"
      ],
      "env": {
        "IMPALA_HOST": "coordinator-default-impala.example.com",
        "IMPALA_PORT": "21050",
        "IMPALA_USER": "username",
        "IMPALA_PASSWORD": "password",
        "IMPALA_DATABASE": "default"
      }
    }
  }
}
```

For Option 2, replace `/path/to` with your path to this repository. Set the environment variables according to your Impala configuration.

## Usage with AI frameworks

The `./examples` folder contains the examples how to integrate this MCP Server with common AI Frameworks like LangChain/LangGraph based agents. This is very basic example without any user interactivity and without chat history just to explain.

### Transport

The MCP server's transport protocol is configurable via the `MCP_TRANSPORT` environment variable. Supported values:
- `stdio` **(default)** — communicate over standard input/output. Useful for local tools, command-line scripts, and integrations with clients like Claude Desktop.
- `http` - expose an HTTP server. Useful for web-based deployments, microservices, exposing MCP over a network.
- `sse` — use Server-Sent Events (SSE) transport. Useful for existing web-based deployments that rely on SSE.

