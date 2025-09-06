import os
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

from hive_mcp_server.tools import impala_tools

mcp = FastMCP(name="Cloudera Hive MCP Server via Impala")


# Register functions as MCP tools
@mcp.tool()
def execute_query(query: str) -> str:
    """
    Execute a SQL query on the Impala database and return results as JSON.
    """
    return impala_tools.execute_query(query)


@mcp.tool()
def show_tables() -> str:
    """
    Retrieve the list of table names in the current Impala database.
    """
    return impala_tools.show_tables()


def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    port = int(os.getenv("MCP_PORT", "8002"))  # Use port 8002 as default instead of 8000
    if transport == "http":
        print(f"Starting Hive MCP Server via transport: {transport} on port {port}")
        mcp.run(transport=transport, port=port)
    else:
        print(f"Starting Hive MCP Server via transport: {transport}")
        mcp.run(transport=transport)

if __name__ == "__main__":
    main()
