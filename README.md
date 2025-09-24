# Github Issues MCP Server

## Overview

Nicely structured MCP Server to work with Github issues.

## How to use

Run the server with `uvx`

```shell
uvx --from  git+https://github.com/phoenyx08/mcp-github-issues mcp-github-issues
```

## Example Client

1. Copy the following to client.py

```python
# client.py

import asyncio
import os

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from dotenv import load_dotenv

load_dotenv()

async def main():
    async with stdio_client(
        StdioServerParameters(command="uvx",
                              args=["--from", "git+https://github.com/phoenyx08/mcp-github-issues", "mcp-github-issues"],
                              env={"GITHUB_PAT": os.getenv("GITHUB_PAT")})
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

            # Call the get_issue tool
            result = await session.call_tool("get_issue", {
                "vendor": "phoenyx08",
                "repository": "mcp-github-issues",
                "issue_id":1
            })
            print(result)

asyncio.run(main())
```

2. Rename .env.example to .env `cp .env.example .env`

3. Edit `GITHUB_PAT` value in `.env`

4. Run with `uv run client.py`
