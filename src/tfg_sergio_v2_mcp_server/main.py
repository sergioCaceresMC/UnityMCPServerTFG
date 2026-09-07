"""Command-line entry point for the Unity MCP server."""


def main() -> None:
    """Start the server once it is wired to the Unity bridge."""
    from utils.mcp_example import mcp

    mcp.run(transport="streamable-http", host="127.0.0.1", port=3001)
