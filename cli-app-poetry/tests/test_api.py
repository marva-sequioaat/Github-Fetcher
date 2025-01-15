import pytest
import sys
from cli_app_poetry.fetchers.api import fetch_github_repo_data
import requests
import requests_mock


# Sample mock data for our tests
MOCK_REPO_DATA = {
    "stargazers_count": 100,
    "forks_count": 50
}

MOCK_BRANCHES_DATA = [
    {"name": "main"},
    {"name": "develop"}
]

MOCK_COMMITS_DATA = [
    {"sha": "abc123", "commit": {"message": "First commit"}},
    {"sha": "def456", "commit": {"message": "Second commit"}}
]

def test_successful_single_repo(capsys, requests_mock):
    """Test fetching data for a single repository with successful responses."""
    # Mock the API endpoints
    requests_mock.get(
        "https://api.github.com/repos/testuser/testrepo",
        json=MOCK_REPO_DATA
    )
    requests_mock.get(
        "https://api.github.com/repos/testuser/testrepo/branches",
        json=MOCK_BRANCHES_DATA
    )
    requests_mock.get(
        "https://api.github.com/repos/testuser/testrepo/commits",
        json=MOCK_COMMITS_DATA
    )

    # Call the function
    fetch_github_repo_data("testuser", ["testrepo"])
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Assert expected output is present
    assert "Fetching data for repository: testrepo" in captured.out
    assert "Branches: 2" in captured.out
    assert "Commits (latest 30): 2" in captured.out
    assert "Total Stars: 100" in captured.out
    assert "Total Forks: 50" in captured.out

def test_multiple_repos(capsys, requests_mock):
    """Test fetching data for multiple repositories."""
    repos = ["repo1", "repo2"]
    
    # Mock responses for each repo
    for repo in repos:
        requests_mock.get(
            f"https://api.github.com/repos/testuser/{repo}",
            json=MOCK_REPO_DATA
        )
        requests_mock.get(
            f"https://api.github.com/repos/testuser/{repo}/branches",
            json=MOCK_BRANCHES_DATA
        )
        requests_mock.get(
            f"https://api.github.com/repos/testuser/{repo}/commits",
            json=MOCK_COMMITS_DATA
        )

    # Call the function
    fetch_github_repo_data("testuser", repos)
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Assert expected output for both repos
    assert "Total Stars: 200" in captured.out  # 100 stars × 2 repos
    assert "Total Forks: 100" in captured.out  # 50 forks × 2 repos

def test_failed_repo_request(capsys, requests_mock):
    """Test handling of failed repository request."""
    # Mock a failed response
    requests_mock.get(
        "https://api.github.com/repos/testuser/testrepo",
        status_code=404
    )

    with pytest.raises(SystemExit) as exc_info:
        fetch_github_repo_data("testuser", ["testrepo"])
    
    assert exc_info.value.code == 6  # Check if system exit code matches

def test_failed_api_call(capsys, requests_mock):
    """Test handling of unexpected API error."""
    # Mock a request that raises an exception
    requests_mock.get(
        "https://api.github.com/repos/testuser/testrepo",
        exc=requests.exceptions.RequestException("Network error")
    )

    with pytest.raises(SystemExit) as exc_info:
        fetch_github_repo_data("testuser", ["testrepo"])
    
    assert exc_info.value.code == 99  # Check if system exit code matches