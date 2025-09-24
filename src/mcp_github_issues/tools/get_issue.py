# src/tools/get_issue.py

from src.mcp_github_issues.utils.get_request import make_get_request


async def get_issue(vendor: str, repository: str, issue_id: int) -> dict:
    """Fetch a complete GitHub issue structure or return an error object.

    Args:
        vendor (str): GitHub username or org name
        repository (str): Repository name
        issue_id (int): Issue number

    Returns:
        dict: Full GitHub issue JSON if successful,
              or {"error": "..."} if an error occurred.
    """

    url = f"https://api.github.com/repos/{vendor}/{repository}/issues/{issue_id}"

    data = await make_get_request(url)

    # If make_get_request returned an error object, propagate it
    if not data or "error" in data:
        return {"error": data.get("error", "Unknown error occurred while fetching issue.")}

    # Success: return full issue JSON
    return data
