import os
import requests
import json
from dateutil.parser import parse as date_parser
from datetime import datetime, timedelta

repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {token}"
}

one_week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"

response = requests.get(f"https://api.github.com/repos/{repo}/branches", headers=headers)

# Check if the response is successful
if response.status_code == 200:
    branches = response.json()

    stale_branch_found = False

    # Iterate over the branches
    for branch in branches:
        branch_name = branch['name']

        # Skip these branches
        if branch_name in ["main", "master", "dev", "development", "dev-iteration"]:
            continue

        # Get the branch info
        branch_info = requests.get(f"https://api.github.com/repos/{repo}/branches/{branch_name}", headers=headers).json()

        # Get the date of the last commit
        last_commit_date = branch_info['commit']['commit']['committer']['date']

        # Check if the last commit is older than one week
        if date_parser(last_commit_date) < date_parser(one_week_ago):
            stale_branch_found = True
            new_branch_name = "archive/" + branch_name
            print(branch_name + " renamed to: " + new_branch_name)

    if not stale_branch_found:
        print("No stale branches to archive")

else:
    print(f"Failed to fetch branches: {response.status_code}")
