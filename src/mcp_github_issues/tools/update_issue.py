from ..utils.patch_request import make_patch_request

async def update_issue(vendor: str, repository: str, issue_id: int, payload: str) -> dict:
    """Update a complete GitHub issue structure and return the issue itself or an error object.

    Args:
        vendor (str): GitHub username or org name also known as owner. Example vendor: phoenyx08
        repository (str): Repository name. Example repository name: mcp-github-issues
        issue_id (int): Issue number. Example issue_id: 4
        payload (str): json string containing changes in the GitHub issue. Example payload: {"title":"Found a bug","body":"I'\''m having a problem with this.","assignees":["octocat"],"milestone":1,"state":"open","labels":["bug"]}

    Returns:
        dict: Full GitHub issue JSON if successful,
              or {"error": "..."} if an error occurred.
    """

    url = f"https://api.github.com/repos/{vendor}/{repository}/issues/{issue_id}"

    data = await make_patch_request(url, payload)

    # If make_patch_request returned an error object, propagate it
    if not data or "error" in data:
        return {
            "error": data.get("error", "Unknown error occurred while fetching issue."),
            "status_code": data["status_code"],
            "details": data["details"],
        }

    # Success: return full issue JSON
    return data
