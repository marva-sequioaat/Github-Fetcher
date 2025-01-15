# FETGitHub

# What is this project?
This CLI tool validates configuration files that will be used to fetch metrics (like branches, commits, stars, forks) from GitHub repositories. It checks if your input JSON file is properly formatted and contains valid data.


# Project Files

cd cli-app-poetry/cli_app_poetry

main.py: Main program that reads and validates the JSON file
validators/github_validator.py: Contains all validation rules for GitHub data
validators/sample.json: Example file showing how your input should look
tests/test_input_validation.py: Test cases to verify the validators work correctly
fetchers/api.py- Contains function that calls Github api and fetch data



## Install Dependencies

To install the dependencies for this project, make sure you have **Poetry** installed. You can install it by running the following command:

pipx install poetry


# create json file in the following format

{
    "username": "github_username",
    "repositories": ["repo1", "repo2"]
}

# setting up the project
after cloning this project,you need to run the following commands to set up the poetry app

cd ..

poetry install

to activate the virtual env give the command

poetry env activate


this will prints the activate command of the virtual environment to the console. Manually copy paste the command and run them to activate venv

# run the program

cd cli_app_poetry

python main.py --config your_config.json

# Testing

to run test give the following command

cd ..

pytest -svv tests

# Exit code
 0 -Success:The operation completed successfully without any errors.
 1 -Failure:No arguments were provided, or required arguments are missing.
 2 -Failure:The specified file was not found or does not exist.
 3 -Failure:The provided JSON file has invalid formatting.
 4 -Failure:The JSON file does not conform to the required schema.
 5 -Failure:The GitHub-specific validations failed for the provided configuration.
 99 -Failure:An unexpected error occurred during execution.