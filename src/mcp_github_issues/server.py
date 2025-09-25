# src/mcp_github_issues/server.py

from mcp.server import FastMCP
from .tools.get_issue import get_issue
from .tools.update_issue import update_issue

mcp = FastMCP("mcp-github-issues")
mcp.add_tool(get_issue)
mcp.add_tool(update_issue)

def main():
    """Entry point for uvx (console script)."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
