# FETGitHub

# What is this project?
This CLI tool validates configuration files that will be used to fetch metrics (like branches, commits, stars, forks) from GitHub repositories. It checks if your input JSON file is properly formatted and contains valid data.


# Project Files

cd cli-app

main.py: Main program that reads and validates the JSON file
github_validator.py: Contains all validation rules for GitHub data
sample_config.json: Example file showing how your input should look
tests/tests_validator.py: Test cases to verify the validators work correctly


# How to use

Make sure you have Python installed
Install required packages:

pip install -r requirments.txt


# create json file in the following format

{
    "username": "github_username",
    "repositories": ["repo1", "repo2"],
    "path": {
        "output_path": "./output",
        "log_path": "./logs"
    },
    "timeout": 30,
    "metrics": {
        "branches": true,
        "forks": true,
        "stars": true,
        "commits": true
    }
}


# run the program

python main.py --config your_config.json

# Testing

to run test give the following command

python -m pytest tests/tests_validator.py -v