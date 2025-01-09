import re
import os
from typing import List, Dict, Union

class GitHubValidators:

    # Class attributes for constants
    USERNAME_REGEX = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){2,38}$'
    REPO_NAME_REGEX = r'^[a-zA-Z0-9._-]+$'
    TIMEOUT_MIN = 10
    TIMEOUT_MAX = 60
    VALID_METRICS = {'forks', 'branches', 'commits', 'stars'}

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate GitHub username according to GitHub standards.
        - Alphanumeric characters and single hyphens only
        - No consecutive hyphens
        - No hyphens at start/end
        - Length: 4-39 characters
        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
            
        # Check length
        if not 4 <= len(username) <= 39:
            raise ValueError("Username must be between 4 and 39 characters")
            
        # Check pattern
       
        if not re.match(GitHubValidators.USERNAME_REGEX, username):
            raise ValueError("Invalid username format. Use only alphanumeric characters and single hyphens (not at start/end)")
            
        return True

    @staticmethod
    def validate_repository_name(repo_name: str) -> bool:
        """
        Validate repository name.
        - Length: 1-100 characters
        - Allowed characters: alphanumeric, -, _, .
        - Cannot end with .
        """
        if not isinstance(repo_name, str):
            raise ValueError("Repository name must be a string")
            
        # Check length
        if not 1 <= len(repo_name) <= 100:
            raise ValueError("Repository name must be between 1 and 100 characters")
            
        # Check if ends with dot
        if repo_name.endswith('.'):
            raise ValueError("Repository name cannot end with a dot")
            
        # Check pattern
        if not re.match(GitHubValidators.REPO_NAME_REGEX, repo_name):
            raise ValueError("Invalid repository name. Use only alphanumeric characters, hyphens, underscores, and dots")
            
        return True

    @staticmethod
    def validate_repository_list(repos: List[str]) -> bool:
        """
        Validate repository list.
        - Must be array of valid repository names
        - Min repos: 1
        - Max repos: 10
        """
        if not isinstance(repos, list):
            raise ValueError("Repositories must be provided as a list")
            
        # Check list length
        if not 1 <= len(repos) <= 10:
            raise ValueError("Number of repositories must be between 1 and 10")
            
        # Validate each repository name
        for repo in repos:
            GitHubValidators.validate_repository_name(repo)
            
        return True

    @staticmethod
    def validate_path(path: str, check_writable: bool = True) -> bool:
        """
        Validate path.
        - Must be a valid path string
        - Must be writable if check_writable is True
        """
        if not isinstance(path, str):
            raise ValueError("Path must be a string")
            
        # Convert to absolute path if relative
        abs_path = os.path.abspath(path)
        
        # Check if parent directory exists and is writable
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
        Validate metrics configuration.
        - Must have correct options (forks, branches, commits, stars)
        - At least one must be True
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
        Validate timeout value.
        - Range: 10-60 seconds
        - Type: integer
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
        Validate entire configuration dictionary.
        Raises ValueError with specific error message if validation fails.
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