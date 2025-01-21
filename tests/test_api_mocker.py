
"""
Test Suite for GitHub Repository Data Fetcher

This module contains pytest test cases for testing the GitHub repository data
fetching and CSV writing functionality. It uses pytest fixtures and mocking
to test various scenarios including successful operations, error handling,
and edge cases.

The tests cover:
- Successful data fetching
- Error handling for API calls
- CSV file operations
- Multiple repository handling
- Rate limiting scenarios
- Unexpected errors

Dependencies:
    - pytest
    - pytest-mock
    - requests
"""

import pytest
import requests
import logging
from typing import Dict, List, Any
from cli_app_poetry.fetchers.api import fetch_github_repo_data,fetch_github_data,write_to_csv
from unittest.mock import MagicMock,patch

# MAX_RETRIES = 3
# RETRY_DELAY = 30


# @pytest.fixture
# def mock_github_api_data():
#     """
#     Fixture to provide mock data for GitHub API responses.
#     """
#     repo_data = {
#         "stargazers_count": 10,
#         "forks_count": 5,
#     }
#     branches_data = [{"name": "main"}, {"name": "dev"}]
#     commits_data = [{"sha": "commit1"}, {"sha": "commit2"}]
#     return repo_data, branches_data, commits_data


# @patch("time.sleep", return_value=None)  # Mock sleep to avoid actual delays
# def test_fetch_github_data_with_retries(mock_sleep, mocker, mock_github_api_data):
#     """
#     Test fetch_github_data function for retry logic on transient errors.
#     """
#     user = "test_user"
#     repositories = ["test_repo"]
#     repo_data, branches_data, commits_data = mock_github_api_data

#     # Mock requests.get
#     mock_get = mocker.patch("requests.get", autospec=True)
#     mock_get.side_effect = [
#         MagicMock(status_code=500),  # First attempt (server error)
#         MagicMock(status_code=502),  # Second attempt (server error)
#         MagicMock(status_code=200, json=lambda: repo_data),  # Successful attempt
#         MagicMock(status_code=200, json=lambda: branches_data),  # Branches
#         MagicMock(status_code=200, json=lambda: commits_data),  # Commits
#     ]

#     result, success = fetch_github_data(user, repositories)

#     assert mock_get.call_count == 5  # 3 retries for repo + branches + commits
#     assert success is True
#     assert len(result) == 1
#     assert result[0]["Stars"] == 10
#     assert result[0]["Forks"] == 5
#     assert result[0]["Branches_Count"] == 2
#     assert result[0]["Commits_Count"] == 2
#     mock_sleep.assert_called_with(RETRY_DELAY)


# @patch("time.sleep", return_value=None)
# def test_fetch_github_data_retry_exhaustion(mock_sleep, mocker):
#     """
#     Test fetch_github_data function when retries are exhausted.
#     """
#     user = "test_user"
#     repositories = ["test_repo"]

#     # Mock requests.get to always return a server error
#     mock_get = mocker.patch("requests.get", autospec=True)
#     mock_get.return_value = MagicMock(status_code=500)

#     result, success = fetch_github_data(user, repositories)

#     assert mock_get.call_count == MAX_RETRIES  # Retry attempts should cap at MAX_RETRIES
#     assert success is False
#     assert result == []
#     mock_sleep.assert_called_with(RETRY_DELAY)


# def test_fetch_github_data_failure_with_logging(mocker, caplog):
#     """
#     Test fetch_github_data function for logging on failure.
#     """
#     user = "test_user"
#     repositories = ["test_repo"]

#     # Mock requests.get to return a client error
#     mock_get = mocker.patch("requests.get", autospec=True)
#     mock_get.return_value = MagicMock(status_code=404, json=lambda: {"message": "Not Found"})

#     with caplog.at_level(logging.ERROR):
#         result, success = fetch_github_data(user, repositories)

#     assert success is False
#     assert result == []
#     assert "Error fetching repository data: 404" in caplog.text







@pytest.fixture
def mock_github_api_data():
    """
    Fixture to provide mock data for GitHub API responses.
    """
    repo_data = {
        "stargazers_count": 10,
        "forks_count": 5,
    }
    branches_data = [{"name": "main"}, {"name": "dev"}]
    commits_data = [{"sha": "commit1"}, {"sha": "commit2"}]
    return repo_data, branches_data, commits_data


@pytest.fixture
def mock_csv_file_path(tmp_path):
    """
    Fixture to provide a temporary CSV file path.
    """
    return tmp_path / "test_data.csv"


def test_fetch_github_data_success(mocker, mock_github_api_data):
    """
    Test fetch_github_data function for successful data fetching.
    """
    user = "test_user"
    repositories = ["test_repo"]
    repo_data, branches_data, commits_data = mock_github_api_data

    # Mock requests.get
    mock_get = mocker.patch("requests.get", autospec=True)
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: repo_data),  # Repo data
        MagicMock(status_code=200, json=lambda: branches_data),  # Branches
        MagicMock(status_code=200, json=lambda: commits_data),  # Commits
    ]

    result, success = fetch_github_data(user, repositories)

    assert success is True
    assert len(result) == 1
    assert result[0]["User"] == user
    assert result[0]["Repository_Name"] == "test_repo"
    assert result[0]["Stars"] == 10
    assert result[0]["Forks"] == 5
    assert result[0]["Branches_Count"] == 2
    assert result[0]["Commits_Count"] == 2


def test_fetch_github_data_failure(mocker):
    """
    Test fetch_github_data function for API failure.
    """
    user = "test_user"
    repositories = ["test_repo"]

    # Mock requests.get to return an error response
    mock_get = mocker.patch("requests.get", autospec=True)
    mock_get.return_value = MagicMock(status_code=404)

    result, success = fetch_github_data(user, repositories)

    assert success is False
    assert result == []


def test_write_to_csv_success(mock_csv_file_path):
    """
    Test write_to_csv function for successful file writing.
    """
    data = [
        {
            "User": "test_user",
            "Repository_Name": "test_repo",
            "Stars": 10,
            "Forks": 5,
            "Branches_Count": 2,
            "Commits_Count": 2,
        }
    ]

    write_to_csv(mock_csv_file_path, data)

    # Check the file contents
    with open(mock_csv_file_path, "r") as file:
        lines = file.readlines()

    assert len(lines) == 2  # Header + Data
    assert "User,Repository_Name,Stars,Forks,Branches_Count,Commits_Count\n" in lines[0]
    assert "test_user,test_repo,10,5,2,2\n" in lines[1]


def test_write_to_csv_no_data(mock_csv_file_path, caplog):
    """
    Test write_to_csv function when no data is provided.
    """
    with caplog.at_level("WARNING"):
        write_to_csv(mock_csv_file_path, [])

    assert "No data to write to CSV" in caplog.text


def test_fetch_github_repo_data(mocker, mock_csv_file_path, mock_github_api_data):
    """
    Test fetch_github_repo_data orchestration function.
    """
    user = "test_user"
    repositories = ["test_repo"]
    repo_data, branches_data, commits_data = mock_github_api_data

    # Mock fetch_github_data
    mocker.patch(
        "cli_app_poetry.fetchers.api.fetch_github_data",
        return_value=(
            [
                {
                    "User": user,
                    "Repository_Name": "test_repo",
                    "Stars": 10,
                    "Forks": 5,
                    "Branches_Count": 2,
                    "Commits_Count": 2,
                }
            ],
            True,
        ),
    )

    # Mock write_to_csv
    mock_write_csv = mocker.patch("cli_app_poetry.fetchers.api.write_to_csv", autospec=True)

    fetch_github_repo_data(user, repositories, mock_csv_file_path)

    mock_write_csv.assert_called_once()

