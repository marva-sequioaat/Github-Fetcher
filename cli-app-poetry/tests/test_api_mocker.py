import pytest
import sys
from cli_app_poetry.fetchers.api import fetch_github_repo_data
import requests

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

def test_successful_single_repo(capsys, mocker):
    """Test fetching data for a single repository with successful responses."""
    # Mock the requests.get method
    mock_get = mocker.patch('requests.get')
    
    # Configure the mock responses
    mock_responses = [
        mocker.Mock(json=lambda: MOCK_REPO_DATA),
        mocker.Mock(json=lambda: MOCK_BRANCHES_DATA),
        mocker.Mock(json=lambda: MOCK_COMMITS_DATA)
    ]
    for response in mock_responses:
        response.status_code = 200
    
    mock_get.side_effect = mock_responses

    # Call the function
    fetch_github_repo_data("testuser", ["testrepo"])
    
    # Verify API calls
    assert mock_get.call_count == 3
    mock_get.assert_has_calls([
        mocker.call("https://api.github.com/repos/testuser/testrepo"),
        mocker.call("https://api.github.com/repos/testuser/testrepo/branches"),
        mocker.call("https://api.github.com/repos/testuser/testrepo/commits")
    ])
    
    # Capture and verify the printed output
    captured = capsys.readouterr()
    assert "Fetching data for repository: testrepo" in captured.out
    assert "Branches: 2" in captured.out
    assert "Commits (latest 30): 2" in captured.out
    assert "Total Stars: 100" in captured.out
    assert "Total Forks: 50" in captured.out

def test_multiple_repos(capsys, mocker):
    """Test fetching data for multiple repositories."""
    repos = ["repo1", "repo2"]
    
    # Mock the requests.get method
    mock_get = mocker.patch('requests.get')
    
    # Configure mock responses for both repos
    mock_responses = []
    for _ in range(len(repos) * 3):  # 3 API calls per repo
        response = mocker.Mock(status_code=200)
        if _ % 3 == 0:
            response.json = lambda: MOCK_REPO_DATA
        elif _ % 3 == 1:
            response.json = lambda: MOCK_BRANCHES_DATA
        else:
            response.json = lambda: MOCK_COMMITS_DATA
        mock_responses.append(response)
    
    mock_get.side_effect = mock_responses

    # Call the function
    fetch_github_repo_data("testuser", repos)
    
    # Verify API calls
    assert mock_get.call_count == 6  # 3 calls × 2 repos
    expected_calls = []
    for repo in repos:
        expected_calls.extend([
            mocker.call(f"https://api.github.com/repos/testuser/{repo}"),
            mocker.call(f"https://api.github.com/repos/testuser/{repo}/branches"),
            mocker.call(f"https://api.github.com/repos/testuser/{repo}/commits")
        ])
    mock_get.assert_has_calls(expected_calls)
    
    # Verify the output
    captured = capsys.readouterr()
    assert "Total Stars: 200" in captured.out  # 100 stars × 2 repos
    assert "Total Forks: 100" in captured.out  # 50 forks × 2 repos

def test_failed_repo_request(capsys, mocker):
    """Test handling of failed repository request."""
    # Mock the requests.get method
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock(status_code=404)
    mock_get.return_value = mock_response

    with pytest.raises(SystemExit) as exc_info:
        fetch_github_repo_data("testuser", ["testrepo"])
    
    # Verify the error handling
    assert exc_info.value.code == 6
    mock_get.assert_called_once_with("https://api.github.com/repos/testuser/testrepo")

def test_failed_api_call(capsys, mocker):
    """Test handling of unexpected API error."""
    # Mock the requests.get method to raise an exception
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    with pytest.raises(SystemExit) as exc_info:
        fetch_github_repo_data("testuser", ["testrepo"])
    
    # Verify the error handling
    assert exc_info.value.code == 99
    mock_get.assert_called_once_with("https://api.github.com/repos/testuser/testrepo")