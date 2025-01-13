import pytest
from cli_app_poetry.validators.github_validator import GitHubValidators

# Initialize the GitHubValidators object for use in tests
validator = GitHubValidators()

def test_valid_username():
    """
    Test case for validating valid GitHub usernames.
    A valid username should pass the following conditions:
    - Contain letters, digits, hyphens, and underscores.
    - Not start or end with a hyphen.
    - Not have consecutive hyphens.
    """
    assert validator.validate_username("john-doe123") == True  # valid username
    assert validator.validate_username("user1234") == True      # valid username with digits

def test_invalid_username():
    """
    Test case for validating invalid GitHub usernames.
    Invalid usernames should raise a ValueError if:
    - The username starts with a hyphen.
    - The username is too short (less than 3 characters).
    - The username contains consecutive hyphens.
    """
    with pytest.raises(ValueError):
        validator.validate_username("-john")  # starts with hyphen
    with pytest.raises(ValueError):
        validator.validate_username("jo")     # too short
    with pytest.raises(ValueError):
        validator.validate_username("john--doe")  # consecutive hyphens

def test_valid_repository_name():
    """
    Test case for validating valid GitHub repository names.
    A valid repository name should pass the following conditions:
    - Contain letters, digits, hyphens, underscores, and periods.
    """
    assert validator.validate_repository_name("my-repo") == True  # valid repository name with hyphen
    assert validator.validate_repository_name("project_1") == True  # valid repository name with underscore
    assert validator.validate_repository_name("test.repo") == True  # valid repository name with period

def test_invalid_repository_name():
    """
    Test case for validating invalid GitHub repository names.
    Invalid repository names should raise a ValueError if:
    - The name ends with a dot.
    - The name contains invalid characters (e.g., `$`).
    """
    with pytest.raises(ValueError):
        validator.validate_repository_name("repo.")  # ends with dot
    with pytest.raises(ValueError):
        validator.validate_repository_name("repo$")  # invalid character '$'


