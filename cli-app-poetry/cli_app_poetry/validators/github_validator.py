"""
GitHub Configuration Validator Module

This module provides validation functionality for GitHub-related configurations through
the GitHubValidators class. It implements comprehensive validation for usernames and
repository names.

The module ensures that all configuration parameters meet GitHub's requirements.added this
"""
import re



class GitHubValidators:
    """A class providing validation methods for GitHub-related configurations."""

    def __init__(self):
        self.username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){2,38}$'
        self.repo_name_regex = r'^[a-zA-Z0-9._-]+$'

    def validate_username(self, username: str) -> bool:
        """Validates a GitHub username against GitHub's username requirements."""
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if not 4 <= len(username) <= 39:
            raise ValueError("Username must be between 4 and 39 characters")
        if not re.match(self.username_regex, username):
            raise ValueError("Invalid username format. Use only alphanumeric characters and single hyphens (not at start/end)")
        return True

    def validate_repository_name(self, repo_name: str) -> bool:
        """Validates a GitHub repository name against naming conventions."""
        if not isinstance(repo_name, str):
            raise ValueError("Repository name must be a string")
        if not 1 <= len(repo_name) <= 100:
            raise ValueError("Repository name must be between 1 and 100 characters")
        if repo_name.endswith('.'):
            raise ValueError("Repository name cannot end with a dot")
        if not re.match(self.repo_name_regex, repo_name):
            raise ValueError("Invalid repository name. Use only alphanumeric characters, hyphens, underscores, and dots")
        return True

    def validate_config(self, config: dict) -> bool:
        """Validates the configuration dictionary."""
        try:
            self.validate_username(config.get('username', ''))
            for repo in config.get('repositories', []):
                self.validate_repository_name(repo)
            return True
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")