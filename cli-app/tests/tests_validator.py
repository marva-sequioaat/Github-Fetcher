# # tests/test_validators.py
# import pytest
# from github_validator import GitHubValidators
# def test_valid_username():
#     assert GitHubValidators.validate_username("john-doe123") == True
#     assert GitHubValidators.validate_username("user1234") == True

# def test_invalid_username():
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_username("-john")  # starts with hyphen
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_username("jo")     # too short
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_username("john--doe")  # consecutive hyphens

# def test_valid_repository_name():
#     assert GitHubValidators.validate_repository_name("my-repo") == True
#     assert GitHubValidators.validate_repository_name("project_1") == True
#     assert GitHubValidators.validate_repository_name("test.repo") == True

# def test_invalid_repository_name():
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_repository_name("repo.")  # ends with dot
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_repository_name("repo$")  # invalid character

# def test_valid_repository_list():
#     assert GitHubValidators.validate_repository_list(["repo1", "repo2"]) == True
#     assert GitHubValidators.validate_repository_list(["single-repo"]) == True

# def test_invalid_repository_list():
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_repository_list([])  # empty list
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_repository_list(["r1", "r2"] * 6)  # too many repos

# def test_valid_metrics():
#     assert GitHubValidators.validate_metrics({
#         "branches": True,
#         "forks": False,
#         "stars": False,
#         "commits": False
#     }) == True

# def test_invalid_metrics():
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_metrics({
#             "branches": False,
#             "forks": False,
#             "stars": False,
#             "commits": False
#         })  # all false
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_metrics({
#             "invalid_metric": True
#         })  # invalid metric name

# def test_valid_timeout():
#     assert GitHubValidators.validate_timeout(30) == True
#     assert GitHubValidators.validate_timeout(10) == True
#     assert GitHubValidators.validate_timeout(60) == True

# def test_invalid_timeout():
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_timeout(5)  # too low
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_timeout(61)  # too high
#     with pytest.raises(ValueError):
#         GitHubValidators.validate_timeout(30.5)  # not an integer