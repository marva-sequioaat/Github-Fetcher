import pytest

from cli_app_poetry.validators.github_validator import GitHubValidators

validator=GitHubValidators()
def test_valid_username():
    assert validator.validate_username("john-doe123") == True
    assert validator.validate_username("user1234") == True

def test_invalid_username():
    with pytest.raises(ValueError):
        validator.validate_username("-john")  # starts with hyphen
    with pytest.raises(ValueError):
        validator.validate_username("jo")     # too short
    with pytest.raises(ValueError):
        validator.validate_username("john--doe")  # consecutive hyphens

def test_valid_repository_name():
    assert validator.validate_repository_name("my-repo") == True
    assert validator.validate_repository_name("project_1") == True
    assert validator.validate_repository_name("test.repo") == True

def test_invalid_repository_name():
    with pytest.raises(ValueError):
        validator.validate_repository_name("repo.")  # ends with dot
    with pytest.raises(ValueError):
        validator.validate_repository_name("repo$")  # invalid character

