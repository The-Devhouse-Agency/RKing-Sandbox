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

one_week_ago = (datetime.utcnow() - timedelta(days=14)).isoformat() + "Z"

stale_branch_found = False

# Initial URL
url = f"https://api.github.com/repos/{repo}/branches"

while url:
    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        branches = response.json()
        
        # Iterate over the branches
        for branch in branches:
            branch_name = branch['name']
            
            # Skip these branches
            if branch_name in ["main", "master", "dev", "development", "dev-iteration"]:
                continue
    
            # Don't rearchive archived branches
            if branch_name.startswith("archive"):
                continue
    
            # Get the branch info
            branch_info = requests.get(f"https://api.github.com/repos/{repo}/branches/{branch_name}", headers=headers).json()
    
            # Skip branches without commits
            if 'commit' not in branch_info or 'commit' not in branch_info['commit'] or 'committer' not in branch_info['commit']['commit']:
                continue
            
            # Get the date of the last commit
            last_commit_date = branch_info['commit']['commit']['committer']['date']
    
            # Check if the last commit is older than one week
            if date_parser(last_commit_date) < date_parser(one_week_ago):
                stale_branch_found = True
                new_branch_name = "archive/" + branch_name
                rename_payload = {"new_name": new_branch_name}
                rename_response = requests.post(f"https://api.github.com/repos/{repo}/branches/{branch_name}/rename", headers=headers, json=rename_payload)
                print(branch_name + " renamed to: " + new_branch_name)
    
        # Check if there is a next page
        if 'next' in response.links:
            url = response.links['next']['url']  # update the URL to the 'next' page URL
        else:
            url = None  # No more pages, break out of the loop

    else:
        print(f"Failed to fetch branches: {response.status_code}")
        break  # Add a break statement to prevent an infinite loop in case of failure

if not stale_branch_found:
    print("No stale branches to archive")
