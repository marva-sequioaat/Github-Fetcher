

"""GitHub Repository Data Fetcher

This script provides functionality to interact with the GitHub API to fetch
details about public repositories. It retrieves the following information for 
each specified repository:

- Number of stars
- Number of forks
- List of branches
- Count of recent commits (up to 30)

The script processes multiple repositories for a given user, aggregates the 
total stars and forks across all repositories, and prints a summary """

import sys
import requests
import csv

GITHUB_API_URL = "https://api.github.com"

def fetch_github_repo_data(user: str, repositories: list, csv_file_path: str) -> None:
    """Fetches stars, forks, commits, and branches for multiple GitHub repos."""
    total_stars = 0
    total_forks = 0
    try:
        headers=["repository name","stars","forks","branches_count","commits_count"]

        #Opening csv file in writer mode
        with open(csv_file_path,mode="w",newline="",encoding="utf-8") as file:
            writer=csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()
            for repo in repositories:
                print(f"\nFetching data for repository: {repo}")
                
                repo_url = f"{GITHUB_API_URL}/repos/{user}/{repo}"
                response = requests.get(repo_url)
                if response.status_code == 200:
                    repo_data = response.json()
                    stars = repo_data['stargazers_count']
                    forks = repo_data['forks_count']
                    total_stars += stars
                    total_forks += forks
                    # Fetch branches
                    branches_url = f"{repo_url}/branches"
                    branches_response = requests.get(branches_url)
                    if branches_response.status_code == 200:
                        branches = branches_response.json()
                        branches_count=len(branches)
                        print(f"  Branches: {len(branches)}")
                    else:
                        print(f"  Error fetching branches: {branches_response.status_code}")

                    # Fetch commits
                    commits_url = f"{repo_url}/commits"
                    commits_response = requests.get(commits_url)
                    if commits_response.status_code == 200:
                        commits = commits_response.json()
                        commits_count=len(commits)

                        #write the data to the csv
                        writer.writerow({
                            "repository name":repo,
                            "stars":stars,
                            "forks":forks,
                            "branches_count":branches_count,
                            "commits_count":commits_count
                        })
                        print(f"  Commits (latest 30): {len(commits)}")
                    else:
                        print(f"  Error fetching commits: {commits_response.status_code}")
                else:
                    print(f"Error fetching data for repository '{repo}': {response.status_code}")
               
        # Print total stars and forks after processing all repositories
        print("\nSummary:")
        print(f"  Total Stars: {total_stars}")
        print(f"  Total Forks: {total_forks}")
    except Exception as e:
        print(f"Unexpected error while fetching GitHub data: {e}")
        sys.exit(99)  # Unexpected error