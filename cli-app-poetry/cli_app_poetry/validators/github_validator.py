"""
GitHub Configuration Validator Module

This module provides validation functionality for GitHub-related configurations through
the GitHubValidators class. It implements comprehensive validation for usernames,
repository names, paths, metrics, and other GitHub-specific parameters.

The module ensures that all configuration parameters meet GitHub's requirements.added this
"""
import re
import os
from typing import List, Dict, Union
class GitHubValidators:
    """
    A class providing validation methods for GitHub-related configurations.
    """

    def __init__(self):
        # Instance attributes for constants
        self.username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){2,38}$'
        self.repo_name_regex = r'^[a-zA-Z0-9._-]+$'
        self.timeout_min = 10
        self.timeout_max = 60
        self.valid_metrics = {'forks', 'branches', 'commits', 'stars'}

    def validate_username(self, username: str) -> bool:
        """
        Validates a GitHub username against GitHub's username requirements.
        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
            
        if not 4 <= len(username) <= 39:
            raise ValueError("Username must be between 4 and 39 characters")
            
        if not re.match(self.username_regex, username):
            raise ValueError("Invalid username format. Use only alphanumeric characters and single hyphens (not at start/end)")
            
        return True

    def validate_repository_name(self, repo_name: str) -> bool:
        """
        Validates a GitHub repository name against naming conventions.
        """
        if not isinstance(repo_name, str):
            raise ValueError("Repository name must be a string")
            
        if not 1 <= len(repo_name) <= 100:
            raise ValueError("Repository name must be between 1 and 100 characters")
            
        if repo_name.endswith('.'):
            raise ValueError("Repository name cannot end with a dot")
            
        if not re.match(self.repo_name_regex, repo_name):
            raise ValueError("Invalid repository name. Use only alphanumeric characters, hyphens, underscores, and dots")
            
        return True

    def validate_repository_list(self, repos: List[str]) -> bool:
        """
        Validates a list of GitHub repository names.
        """
        if not isinstance(repos, list):
            raise ValueError("Repositories must be provided as a list")
            
        if not 1 <= len(repos) <= 10:
            raise ValueError("Number of repositories must be between 1 and 10")
            
        for repo in repos:
            self.validate_repository_name(repo)
            
        return True

    def validate_path(self, path: str, check_writable: bool = True) -> bool:
        """
        Validates a filesystem path and optionally checks write permissions.
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

    def validate_metrics(self, metrics: Dict[str, bool]) -> bool:
        """
        Validates the metrics configuration dictionary.
        """
        if not isinstance(metrics, dict):
            raise ValueError("Metrics must be provided as a dictionary")

        if not self.valid_metrics.issuperset(metrics.keys()):
            raise ValueError("Invalid metrics found.")
        if not any(metrics.values()):
            raise ValueError("At least one metric must be set to true")
        return True

    def validate_timeout(self, timeout: Union[int, float]) -> bool:
        """
        Validates the timeout value for API requests.
        """
        if not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number")
            
        if not isinstance(timeout, int):
            raise ValueError("Timeout must be an integer")
            
        if not self.timeout_min <= timeout <= self.timeout_max:
            raise ValueError(
                f"Timeout must be between {self.timeout_min} and {self.timeout_max} seconds"
            )
            
        return True

    def validate_config(self, config: dict) -> bool:
        """
        Validates the entire configuration dictionary.
        """
        try:
            self.validate_username(config.get('username', ''))
            self.validate_repository_list(config.get('repositories', []))
            
            paths = config.get('path', {})
            self.validate_path(paths.get('output_path', ''))
            self.validate_path(paths.get('log_path', ''))
            
            self.validate_metrics(config.get('metrics', {}))
            self.validate_timeout(config.get('timeout', 0))
            
            return True
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")



