"""
GitHub Configuration Validator Module

This module provides validation functionality for GitHub-related configurations through
the GitHubValidators class. It implements comprehensive validation for usernames,
repository names, paths, metrics, and other GitHub-specific parameters.

The module ensures that all configuration parameters meet GitHub's requirements and
best practices for API interaction and data collection.

"""

import re
import os
from typing import List, Dict, Union

class GitHubValidators:
    """
    A class providing validation methods for GitHub-related configurations.

    This class contains static methods to validate various components of a GitHub
    configuration including usernames, repository names, paths, and metrics settings.
    It ensures all configuration parameters meet GitHub's requirements and practical
    constraints for API interaction.

   
    """

    # Class attributes for constants
    USERNAME_REGEX = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){2,38}$'
    REPO_NAME_REGEX = r'^[a-zA-Z0-9._-]+$'
    TIMEOUT_MIN = 10
    TIMEOUT_MAX = 60
    VALID_METRICS = {'forks', 'branches', 'commits', 'stars'}

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validates a GitHub username against GitHub's username requirements.

        Args:
            username (str): The GitHub username to validate

        Returns:
            bool: True if the username is valid

        Raises:
            ValueError: If the username is invalid, with a specific error message
                detailing the validation failure

        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
            
        if not 4 <= len(username) <= 39:
            raise ValueError("Username must be between 4 and 39 characters")
            
        if not re.match(GitHubValidators.USERNAME_REGEX, username):
            raise ValueError("Invalid username format. Use only alphanumeric characters and single hyphens (not at start/end)")
            
        return True

    @staticmethod
    def validate_repository_name(repo_name: str) -> bool:
        """
        Validates a GitHub repository name against naming conventions.

        Args:
            repo_name (str): The repository name to validate

        Returns:
            bool: True if the repository name is valid

        Raises:
            ValueError: If the repository name is invalid, with a specific error
                message detailing the validation failure

        """
        if not isinstance(repo_name, str):
            raise ValueError("Repository name must be a string")
            
        if not 1 <= len(repo_name) <= 100:
            raise ValueError("Repository name must be between 1 and 100 characters")
            
        if repo_name.endswith('.'):
            raise ValueError("Repository name cannot end with a dot")
            
        if not re.match(GitHubValidators.REPO_NAME_REGEX, repo_name):
            raise ValueError("Invalid repository name. Use only alphanumeric characters, hyphens, underscores, and dots")
            
        return True

    @staticmethod
    def validate_repository_list(repos: List[str]) -> bool:
        """
        Validates a list of GitHub repository names.

        Args:
            repos (List[str]): List of repository names to validate

        Returns:
            bool: True if all repository names are valid

        Raises:
            ValueError: If the repository list is invalid or any repository name
                is invalid, with a specific error message

        """
        if not isinstance(repos, list):
            raise ValueError("Repositories must be provided as a list")
            
        if not 1 <= len(repos) <= 10:
            raise ValueError("Number of repositories must be between 1 and 10")
            
        for repo in repos:
            GitHubValidators.validate_repository_name(repo)
            
        return True

    @staticmethod
    def validate_path(path: str, check_writable: bool = True) -> bool:
        """
        Validates a filesystem path and optionally checks write permissions.

        Args:
            path (str): The filesystem path to validate
            check_writable (bool, optional): Whether to verify write permissions.
                Defaults to True.

        Returns:
            bool: True if the path is valid and writable (if check_writable is True)

        Raises:
            ValueError: If the path is invalid or not writable (when check_writable
                is True), with a specific error message
        """
        
        if not isinstance(path, str):
            raise ValueError("Path must be a string")
            
        abs_path = os.path.abspath(path)
        parent_dir = os.path.dirname(abs_path)
        
        if not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir)
            except Exception as e:
                raise ValueError(f"Cannot create directory {parent_dir}: {str(e)}")
                
        if check_writable:
            if os.path.exists(abs_path):
                if not os.access(abs_path, os.W_OK):
                    raise ValueError(f"Path {path} is not writable")
            else:
                if not os.access(parent_dir, os.W_OK):
                    raise ValueError(f"Directory {parent_dir} is not writable")
                    
        return True

    @staticmethod
    def validate_metrics(metrics: Dict[str, bool]) -> bool:
        """
        Validates the metrics configuration dictionary.

        Args:
            metrics (Dict[str, bool]): Dictionary of metric names and their enabled status

        Returns:
            bool: True if the metrics configuration is valid

        Raises:
            ValueError: If the metrics configuration is invalid, with a specific
                error message

        """
        if not isinstance(metrics, dict):
            raise ValueError("Metrics must be provided as a dictionary")

        if not GitHubValidators.VALID_METRICS.issuperset(metrics.keys()):
            raise ValueError("Invalid metrics found.")
        if not any(metrics.values()):
            raise ValueError("At least one metric must be set to true")
        return True

    @staticmethod
    def validate_timeout(timeout: Union[int, float]) -> bool:
        """
        Validates the timeout value for API requests.

        Args:
            timeout (Union[int, float]): The timeout value in seconds

        Returns:
            bool: True if the timeout value is valid

        Raises:
            ValueError: If the timeout value is invalid, with a specific error message

        """
        if not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number")
            
        if not isinstance(timeout, int):
            raise ValueError("Timeout must be an integer")
            
        if not GitHubValidators.TIMEOUT_MIN <= timeout <= GitHubValidators.TIMEOUT_MAX:
            raise ValueError(
                f"Timeout must be between {GitHubValidators.TIMEOUT_MIN} and {GitHubValidators.TIMEOUT_MAX} seconds"
            )
            
        return True

    @classmethod
    def validate_config(cls, config: dict) -> bool:
        """
        Validates the entire configuration dictionary.

        Performs comprehensive validation of all configuration parameters including
        username, repositories, paths, metrics, and timeout settings.

        Args:
            config (dict): The complete configuration dictionary to validate

        Returns:
            bool: True if the entire configuration is valid

        Raises:
            ValueError: If any part of the configuration is invalid, with a specific
                error message detailing which validation failed

        """
        try:
            cls.validate_username(config.get('username', ''))
            cls.validate_repository_list(config.get('repositories', []))
            
            paths = config.get('path', {})
            cls.validate_path(paths.get('output_path', ''))
            cls.validate_path(paths.get('log_path', ''))
            
            cls.validate_metrics(config.get('metrics', {}))
            cls.validate_timeout(config.get('timeout', 0))
            
            return True
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")

