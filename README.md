# FETGitHub

# What is this project?
This CLI tool validates configuration files that will be used to fetch metrics (like branches, commits, stars, forks) from GitHub repositories. It checks if your input JSON file is properly formatted and contains valid data.


# Project Files

cd 

cli-app-poetry/cli_app_poetry/main.py: Main program that reads and validates the JSON file
cli-app-poetry/cli_app_poetry/validators/github_validator.py: Contains all validation rules for GitHub data
cli-app-poetry/cli_app_poetry/validators/sample.json: Example file showing how your input should look
cli-app-poetry/tests/test_input_validation.py: Test cases to verify the validators work correctly
cli-app-poetry/cli_app_poetry/fetchers/api.py- Contains function that calls Github api and fetch data



# create json file in the following format

{
    "username": "github_username",
    "repositories": ["repo1", "repo2"]
}

# setting up the project
after cloning this project,you need to run the following commands to set up the project

 cd FETGitHub

 Build the Docker image:

 docker build -t cli-app .

# Usage
# Running the CLI Application

The application requires a configuration file and mounts a local directory for data processing.

Basic usage:
docker run  -v /path/to/your/local/directory:/data   <image_id>   cli-app-poetry --config /data/your_input_json_file_name

# Volume Mounting

The -v flag mounts your local directory to the /data directory in the container
Ensure your configuration file is in the mounted directory
Replace /path/to/your/local/directory with your actual local path

# Running Tests
To run the test suite:


docker run <image id>  pytest /app/tests

# Exit code
 0 -Success:The operation completed successfully without any errors.
 1 -Failure:No arguments were provided, or required arguments are missing.
 2 -Failure:The specified file was not found or does not exist.
 3 -Failure:The provided JSON file has invalid formatting.
 4 -Failure:The JSON file does not conform to the required schema.
 5 -Failure:The GitHub-specific validations failed for the provided configuration.
 99 -Failure:An unexpected error occurred during execution.