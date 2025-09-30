import json

from ..utils.patch_request import make_patch_request

async def update_issue_body(vendor: str, repository: str, issue_id: int, body: str) -> str:
    """Update a GitHub issue body only. Returns new body or error message.
       Use this tool, rather they update_issue if you need to update ONLY the issue body.

    Args:
        vendor (str): GitHub username or org name also known as owner. Example vendor: phoenyx08
        repository (str): Repository name. Example repository name: mcp-github-issues
        issue_id (int): Issue number. Example issue_id: 4
        body (str): string containing new body of the GitHub issue. Example body: 'This is new issue body'

    Returns:
        str: Updated body of the GitHub issue. Example: 'This is new issue body'
              or error message e.g. 'Something went wrong' if an error occurred.
    """

    url = f"https://api.github.com/repos/{vendor}/{repository}/issues/{issue_id}"

    payload = json.dumps({"body": body})

    data = await make_patch_request(url, payload)

    # If make_patch_request returned an error object, convert it to string and return
    if not data or "error" in data:
        return "error" + data.get("error", "Unknown error occurred while fetching issue.") \
            + "status_code" + data["status_code"] \
            + "details" + data["details"]

    # Success: return issue title
    return data.get("body")
