
"""
CLI tool for validating GitHub configuration JSON files.
Provides functionality to display sample JSON and validate config files
against a predefined schema and GitHub-specific requirements.
"""

import json
import os
import sys
from typing import Optional
from jsonschema import validate, ValidationError
from cli_app_poetry.validators.schema import schema
from cli_app_poetry.validators.github_validator import GitHubValidators
from cli_app_poetry.fetchers.api import fetch_github_repo_data
from importlib.resources import files
from cli_app_poetry.constants import DEFAULT_SAMPLE_FILE
import logging
import argparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def display_sample_json(file_path: str) -> None:
    """Displays the content of the sample JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = json.load(file)
                logger.info("Sample JSON File Content:")
                # Using print for formatted JSON display since it's actual content, not a log
                print(json.dumps(content, indent=4))
        else:
            logger.error(f"Sample JSON file '{file_path}' not found.")
            sys.exit(2)  # File not found
    except Exception as e:
        logger.error(f"Unexpected error while displaying sample JSON: {e}", exc_info=True)
        sys.exit(99)  # Unexpected error

def validate_json(file_path: str) -> None:
    """Validates a JSON file against schema and GitHub requirements."""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File '{file_path}' not found.")
            sys.exit(2)  # File not found

        with open(file_path, "r") as f:
            data = json.load(f)
           
        # Validate against the schema
        validate(instance=data, schema=schema)
       
        # Perform GitHub-specific validations
        validator = GitHubValidators()
        validator.validate_config(data)

        logger.info("JSON is valid!")
        return data
        
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        sys.exit(2)  # File not found
    except json.JSONDecodeError as e:
        # Detailed error reporting
        logger.error(
            f"Invalid JSON format on line {e.lineno}, column {e.colno}.\n"
            f"Details: {e.msg}"
        )
        sys.exit(3)  # Invalid JSON format
    except ValidationError as e:
        logger.error(f"Schema Validation Error: {e.message}")
        sys.exit(4)  # Schema validation error
    except ValueError as e:
        logger.error(f"Value Error during validation: {e}")
        sys.exit(5)  # GitHub-specific validation error
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}", exc_info=True)
        sys.exit(99)  # Unexpected error

def main():
    try:
        parser = argparse.ArgumentParser(description="CLI JSON Validator")
        parser.add_argument("--show-sample", nargs="?", const=DEFAULT_SAMPLE_FILE, 
                          help="Path to the sample JSON file")
        parser.add_argument("--config", help="Path to the JSON config file to validate")
        args = parser.parse_args()

        # csv_file_path = "/mnt/c/Users/SequoiaAT/Desktop/Marva/github_repo_data.csv"
        csv_file_path = "/data/github_repo_data.csv"
        
        if args.config:
            # Validate config file exists
            config_path = Path(args.config)
            if not config_path.exists():
                logger.error(f"Config file '{args.config}' not found.")
                sys.exit(2)  # File not found
            
            # Validate config file is readable
            if not config_path.is_file():
                logger.error(f"'{args.config}' is not a file.")
                sys.exit(3)  # Not a file
                
            try:
                # Attempt to parse JSON
                data = validate_json(args.config)
            except json.JSONDecodeError as je:
                logger.error(f"Invalid JSON format in '{args.config}': {str(je)}")
                sys.exit(4)  # Invalid JSON format
            except Exception as e:
                logger.error(f"Error reading config file: {str(e)}", exc_info=True)
                sys.exit(99)  # Unexpected error while reading file
            
            username = data.get("username")
            repos = data.get("repositories")
            
            if username and repos:
                if args.show_sample:
                    display_sample_json(args.show_sample)
                try:
                    logger.info(f"Starting GitHub data fetch for user: {username}")
                    fetch_github_repo_data(username, repos, csv_file_path)
                except Exception as e:
                    logger.error(f"Error occurred while fetching GitHub data: {e}", 
                               exc_info=True)
                    sys.exit(99)
            else:
                logger.error("JSON file does not contain 'username' or 'repositories'.")
                sys.exit(5)  # Missing required fields
                
        elif args.show_sample:
            display_sample_json(args.show_sample)
        else:
            logger.error("No arguments provided. Use --show-sample or --config.")
            sys.exit(1)  # No arguments provided

        logger.info("Operation completed successfully.")
        sys.exit(0)  # Success exit code
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(99)