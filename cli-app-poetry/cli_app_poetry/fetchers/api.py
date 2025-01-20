"""
GitHub Repository Data Collection Module

This module provides functionality to fetch and store GitHub repository data.
It collects information such as stars, forks, branch count, and commit count
for specified repositories and stores them in a CSV file.

The module uses the GitHub REST API for data collection and implements
robust error handling and logging mechanisms.

Dependencies:
    - requests
    - csv
    - logging
    - os
    - sys

Typical usage:
    repositories = ['repo1', 'repo2']
    fetch_github_repo_data('username', repositories, 'output.csv')
"""

import requests
import csv
import logging
import os
import sys
from typing import Tuple, List, Dict, Any
from cli_app_poetry.constants import GITHUB_API_URL
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
MAX_RETRIES=3
RETRY_DELAY=30
def fetch_github_data(user: str, repositories: list) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Fetch repository data from GitHub API for specified repositories.

    This function makes API calls to GitHub to collect various metrics for each
    repository including star count, fork count, branch count, and commit count.
    It implements error handling for API failures and rate limiting.

    Args:
        user (str): GitHub username whose repositories are being accessed
        repositories (list): List of repository names to fetch data for

    Returns:
        Tuple[List[Dict[str, Any]], bool]: A tuple containing:
            - List of dictionaries with repository data
            - Boolean indicating if all data was fetched successfully

    Raises:
        requests.exceptions.RequestException: For network-related errors
        ValueError: For invalid input parameters
    """
    repo_data_list = []
    fetch_success = True
    
    for repo in repositories:
        logger.info(f"Fetching data for repository: {repo}")
        try:
            repo_url = f"{GITHUB_API_URL}/repos/{user}/{repo}"
            response = requests.get(repo_url)
            if response.status_code == 200:
                repo_data = response.json()
                stars = repo_data.get('stargazers_count', 0)
                forks = repo_data.get('forks_count', 0)

                # Fetch branches
                branches_url = f"{repo_url}/branches"
                branches_response = requests.get(branches_url)
                if branches_response.status_code != 200:
                    logger.error(f"Error fetching branches data: {branches_response.status_code}")
                    fetch_success = False
                    continue
                branches_count = len(branches_response.json())

                # Fetch commits
                commits_url = f"{repo_url}/commits"
                commits_response = requests.get(commits_url)
                if commits_response.status_code != 200:
                    logger.error(f"Error fetching commits data: {commits_response.status_code}")
                    fetch_success = False
                    continue
                commits_count = len(commits_response.json())

                repo_data_list.append({
                    "User": user,
                    "Repository_Name": repo,
                    "Stars": stars,
                    "Forks": forks,
                    "Branches_Count": branches_count,
                    "Commits_Count": commits_count
                })
            else:
                logger.error(f"Error fetching repository data: {response.status_code}")
                fetch_success = False
                
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {repo}: {e}", exc_info=True)
            fetch_success = False
            
    return repo_data_list, fetch_success

def write_to_csv(csv_file_path: str, data: list) -> None:
    """
    Write repository data to a CSV file.

    This function handles the storage of collected GitHub repository data
    into a CSV file, with support for both creating new files and
    appending to existing ones.

    Args:
        csv_file_path (str): Path to the CSV file where data will be written
        data (list): List of dictionaries containing repository data

    Raises:
        OSError: For file system related errors
        Exception: For other unexpected errors during file operations
    """
    if not data:
        logger.warning("No data to write to CSV")
        return
        
    headers = ["User", "Repository_Name", "Stars", "Forks", "Branches_Count", "Commits_Count"]
    try:
        file_exists = os.path.exists(csv_file_path)
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)
        logger.info(f"Data successfully written to {csv_file_path}")
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}", exc_info=True)
        sys.exit(99)

def fetch_github_repo_data(user: str, repositories: list, csv_file_path: str) -> None:
    """
    Main orchestration function for GitHub data collection and storage.

    This function coordinates the entire process of fetching GitHub repository
    data and storing it in a CSV file. It handles the high-level workflow
    and error management.

    Args:
        user (str): GitHub username whose repositories are being accessed
        repositories (list): List of repository names to fetch data for
        csv_file_path (str): Path to the CSV file where data will be written

    Raises:
        Exception: For any unexpected errors during execution
    """
    try:
        logger.info(f"Starting data collection for user: {user}")
        processed_data, fetch_success = fetch_github_data(user, repositories)
        
        if fetch_success and processed_data:
            write_to_csv(csv_file_path, processed_data)
        else:
            logger.error("Skipping CSV write due to fetch errors or no data")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error while processing GitHub data: {e}", exc_info=True)
        sys.exit(99)


