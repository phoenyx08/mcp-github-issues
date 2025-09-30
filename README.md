# GitHub Issues MCP Server

## Overview

Nicely structured MCP Server to work with GitHub issues.

### Available tools

- `get_issue` - returns complete issue
- `update_issue` - updates complete issue
- `update_issue_title` - updates the issue title only
- `update_issue_body` - updates the issue body only

## How to use

Run the server with `uvx`

```shell
uvx --from  git+https://github.com/phoenyx08/mcp-github-issues mcp-github-issues
```

## Example Client

1. Copy the following to client.py

```python
import asyncio
import json
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

            # Get Issue
            result = await session.call_tool("get_issue", {
                "vendor": "phoenyx08",
                "repository": "mcp-github-issues",
                "issue_id":1
            })
            print(result)

            # Update Issue
            result = await session.call_tool("get_issue", {
                "vendor": "phoenyx08",
                "repository": "mcp-github-issues",
                "issue_id": 4
            })
            data = json.loads(result.content[0].text)
            body = data["body"]
            title = data["title"]
            new_body = body + "\nThis issue was updated\n"
            payload = {"body": new_body}
            payload = json.dumps(payload)

            # Call the update_issue tool
            result = await session.call_tool("update_issue", {
                "vendor": "phoenyx08",
                "repository": "mcp-github-issues",
                "issue_id": 4,
                "payload": payload
            })
            print(result)

            # Update Issue Title
            print("Original Title: " + title)
            title = title + " (updated)"
            # Call the update_issue_title tool
            result = await session.call_tool("update_issue_title", {
                "vendor": "phoenyx08",
                "repository": "mcp-github-issues",
                "issue_id": 4,
                "title": title
            })
            data = result.content[0].text
            print("New title: " + data)
            
            # Update Issue Body works the same as Update Issue Title

asyncio.run(main())

```

2. Rename .env.example to .env `cp .env.example .env`

3. Edit `GITHUB_PAT` value in `.env`

4. Run with `uv run client.py`
