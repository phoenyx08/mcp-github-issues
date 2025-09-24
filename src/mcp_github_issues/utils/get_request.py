# src/utils/get_request.py

from typing import Any
from ..config import config
import httpx

GITHUB_PAT = config.github_pat
USER_AGENT = config.user_agent

async def make_get_request(url: str) -> dict[str, Any] | None:
    """Make a request to the GitHub API with proper error handling."""

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    }

    if GITHUB_PAT:
        headers["Authorization"] = f"Bearer {GITHUB_PAT}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)

            if response.status_code == 401:
                return {"error": "Unauthorized. Invalid or missing GitHub token."}

            if response.status_code == 403:
                # GitHub often uses 403 for rate-limiting too
                if "X-RateLimit-Remaining" in response.headers and response.headers.get("X-RateLimit-Remaining") == "0":
                    return {"error": "Rate limit exceeded. Please wait before retrying."}
                return {"error": "Forbidden. You may not have permission to access this resource."}

            if response.status_code == 404:
                return {"error": "Not Found. Issue or repository does not exist."}

            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            return {"error": f"Network error while requesting GitHub: {str(e)}"}

        except httpx.HTTPStatusError as e:
            return {"error": f"Unexpected HTTP error from GitHub: {str(e)}"}

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
