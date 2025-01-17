import pytest
import requests
from unittest.mock import mock_open, patch
from cli_app_poetry.fetchers.api import fetch_github_repo_data

@pytest.fixture
def sample_repo_data():
    return {
        "stargazers_count": 100,
        "forks_count": 50
    }

@pytest.fixture
def sample_branches_data():
    return [
        {"name": "main"},
        {"name": "develop"}
    ]

@pytest.fixture
def sample_commits_data():
    return [
        {"sha": "abc123", "commit": {"message": "First commit"}},
        {"sha": "def456", "commit": {"message": "Second commit"}}
    ]

@pytest.fixture
def mock_csv_file(mocker):
    return mock_open()

def test_successful_fetch(mocker, sample_repo_data, sample_branches_data, sample_commits_data, mock_csv_file):
    """Test successful fetching of repository data"""
    # Mock the CSV file operations
    mocker.patch("builtins.open", mock_csv_file)
    mocker.patch("os.path.exists", return_value=False)
    
    # Mock all API responses
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    
    def get_mock_response(*args, **kwargs):
        if "/repos/testuser/testrepo" in args[0]:
            mock_response.json.return_value = sample_repo_data
        elif "/branches" in args[0]:
            mock_response.json.return_value = sample_branches_data
        elif "/commits" in args[0]:
            mock_response.json.return_value = sample_commits_data
        return mock_response
    
    mocker.patch("requests.get", side_effect=get_mock_response)
    
    # Run the function
    
    fetch_github_repo_data("testuser", ["testrepo"], "test.csv")
    
    # Verify CSV file was opened
    mock_csv_file.assert_called_with("test.csv", mode="a", newline="", encoding="utf-8")
    
    # Verify API calls were made
    requests.get.assert_any_call("https://api.github.com/repos/testuser/testrepo")
    requests.get.assert_any_call("https://api.github.com/repos/testuser/testrepo/branches")
    requests.get.assert_any_call("https://api.github.com/repos/testuser/testrepo/commits")

def test_repo_not_found(mocker, mock_csv_file):
    """Test handling of repository not found"""
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("builtins.open", mock_csv_file)
    
    # Mock 404 response
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)
    
    # Run the function

    fetch_github_repo_data("testuser", ["nonexistent-repo"], "test.csv")
    
    # Verify only one API call was made (subsequent calls shouldn't happen after 404)
    assert requests.get.call_count == 1

def test_api_rate_limit_exceeded(mocker, mock_csv_file):
    """Test handling of GitHub API rate limit"""
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("builtins.open", mock_csv_file)
    
    # Mock 403 rate limit response
    mock_response = mocker.Mock()
    mock_response.status_code = 403
    mocker.patch("requests.get", return_value=mock_response)
    
    # Run the function
 
    fetch_github_repo_data("testuser", ["testrepo"], "test.csv")
    
    # Verify error handling
    assert requests.get.call_count == 1

def test_multiple_repositories(mocker, sample_repo_data, sample_branches_data, sample_commits_data, mock_csv_file):
    """Test fetching data for multiple repositories"""
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("builtins.open", mock_csv_file)
    
    # Mock successful responses
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        sample_repo_data,
        sample_branches_data,
        sample_commits_data,
        sample_repo_data,  # For second repo
        sample_branches_data,
        sample_commits_data
    ]
    
    mocker.patch("requests.get", return_value=mock_response)
    
    # Run the function
    fetch_github_repo_data("testuser", ["repo1", "repo2"], "test.csv")
    
    # Verify multiple repos were processed
    assert requests.get.call_count == 6  # 3 API calls per repo

def test_file_handling(mocker, sample_repo_data, sample_branches_data, sample_commits_data, mock_csv_file):
    """Test CSV file handling"""
    # Test with existing file
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mock_csv_file)
    
    # Mock successful API responses
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = [
        sample_repo_data,
        sample_branches_data,
        sample_commits_data
    ]
    
    mocker.patch("requests.get", return_value=mock_response)
    
    # Run the function
    fetch_github_repo_data("testuser", ["testrepo"], "test.csv")
    
    # Verify file operations
    mock_csv_file.assert_called_with("test.csv", mode="a", newline="", encoding="utf-8")

def test_unexpected_error(mocker):
    """Test handling of unexpected errors"""
    mocker.patch("os.path.exists", side_effect=Exception("Unexpected error"))
    
    # Run the function and check for system exit
    with pytest.raises(SystemExit) as exc_info:
        fetch_github_repo_data("testuser", ["testrepo"], "test.csv")
    
    assert exc_info.value.code == 99


# import pytest
# import sys
# from cli_app_poetry.fetchers.api import fetch_github_repo_data
# import requests

# # Sample mock data for our tests
# MOCK_REPO_DATA = {
#     "stargazers_count": 100,
#     "forks_count": 50
# }

# MOCK_BRANCHES_DATA = [
#     {"name": "main"},
#     {"name": "develop"}
# ]

# MOCK_COMMITS_DATA = [
#     {"sha": "abc123", "commit": {"message": "First commit"}},
#     {"sha": "def456", "commit": {"message": "Second commit"}}
# ]

# def test_successful_single_repo(capsys, mocker):
#     """Test fetching data for a single repository with successful responses."""
#     # Mock the requests.get method
#     mock_get = mocker.patch('requests.get')
    
#     # Configure the mock responses
#     mock_responses = [
#         mocker.Mock(json=lambda: MOCK_REPO_DATA),
#         mocker.Mock(json=lambda: MOCK_BRANCHES_DATA),
#         mocker.Mock(json=lambda: MOCK_COMMITS_DATA)
#     ]
#     for response in mock_responses:
#         response.status_code = 200
    
#     mock_get.side_effect = mock_responses

#     # Call the function
#     fetch_github_repo_data("testuser", ["testrepo"])
    
#     # Verify API calls
#     assert mock_get.call_count == 3
#     mock_get.assert_has_calls([
#         mocker.call("https://api.github.com/repos/testuser/testrepo"),
#         mocker.call("https://api.github.com/repos/testuser/testrepo/branches"),
#         mocker.call("https://api.github.com/repos/testuser/testrepo/commits")
#     ])
    
#     # Capture and verify the printed output
#     captured = capsys.readouterr()
#     assert "Fetching data for repository: testrepo" in captured.out
#     assert "Branches: 2" in captured.out
#     assert "Commits (latest 30): 2" in captured.out
#     assert "Total Stars: 100" in captured.out
#     assert "Total Forks: 50" in captured.out

# def test_multiple_repos(capsys, mocker):
#     """Test fetching data for multiple repositories."""
#     repos = ["repo1", "repo2"]
    
#     # Mock the requests.get method
#     mock_get = mocker.patch('requests.get')
    
#     # Configure mock responses for both repos
#     mock_responses = []
#     for _ in range(len(repos) * 3):  # 3 API calls per repo
#         response = mocker.Mock(status_code=200)
#         if _ % 3 == 0:
#             response.json = lambda: MOCK_REPO_DATA
#         elif _ % 3 == 1:
#             response.json = lambda: MOCK_BRANCHES_DATA
#         else:
#             response.json = lambda: MOCK_COMMITS_DATA
#         mock_responses.append(response)
    
#     mock_get.side_effect = mock_responses

#     # Call the function
#     fetch_github_repo_data("testuser", repos)
    
#     # Verify API calls
#     assert mock_get.call_count == 6  # 3 calls × 2 repos
#     expected_calls = []
#     for repo in repos:
#         expected_calls.extend([
#             mocker.call(f"https://api.github.com/repos/testuser/{repo}"),
#             mocker.call(f"https://api.github.com/repos/testuser/{repo}/branches"),
#             mocker.call(f"https://api.github.com/repos/testuser/{repo}/commits")
#         ])
#     mock_get.assert_has_calls(expected_calls)
    
#     # Verify the output
#     captured = capsys.readouterr()
#     assert "Total Stars: 200" in captured.out  # 100 stars × 2 repos
#     assert "Total Forks: 100" in captured.out  # 50 forks × 2 repos

# def test_failed_repo_request(capsys, mocker):
#     """Test handling of failed repository request."""
#     # Mock the requests.get method
#     mock_get = mocker.patch('requests.get')
#     mock_response = mocker.Mock(status_code=404)
#     mock_get.return_value = mock_response

#     with pytest.raises(SystemExit) as exc_info:
#         fetch_github_repo_data("testuser", ["testrepo"])
    
#     # Verify the error handling
#     assert exc_info.value.code == 6
#     mock_get.assert_called_once_with("https://api.github.com/repos/testuser/testrepo")

# def test_failed_api_call(capsys, mocker):
#     """Test handling of unexpected API error."""
#     # Mock the requests.get method to raise an exception
#     mock_get = mocker.patch('requests.get')
#     mock_get.side_effect = requests.exceptions.RequestException("Network error")

#     with pytest.raises(SystemExit) as exc_info:
#         fetch_github_repo_data("testuser", ["testrepo"])
    
#     # Verify the error handling
#     assert exc_info.value.code == 99
#     mock_get.assert_called_once_with("https://api.github.com/repos/testuser/testrepo")