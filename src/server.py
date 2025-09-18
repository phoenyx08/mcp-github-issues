# src/server.py

from mcp.server import FastMCP
from src.tools.get_issue import get_issue

mcp = FastMCP("mcp-github-issues")

mcp.add_tool(get_issue)

if __name__ == "__main__":
    mcp.run(transport='stdio')
