
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
from validators.schema import schema
from validators.github_validator import GitHubValidators
from fetchers.api import fetch_github_repo_data
from importlib.resources import files
from constants import DEFAULT_SAMPLE_FILE

def display_sample_json(file_path: str) -> None:
    """Displays the content of the sample JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = json.load(file)
                print("\nSample JSON File Content:")
                print(json.dumps(content, indent=4))
        else:
            print(f"Error: Sample JSON file '{file_path}' not found.")
            sys.exit(2) # File not found
    except Exception as e:
        print(f"Unexpected error while displaying sample JSON: {e}")
        sys.exit(99) # Unexpected error

def validate_json(file_path: str) -> None:
    """Validates a JSON file against schema and GitHub requirements."""
    try:
        if not os.path.exists(file_path):
            # raise FileNotFoundError(f"File '{file_path}' not found.")
            print(f"File '{file_path}' not found.")
            sys.exit(2)  # File not found
        with open(file_path, "r") as f:
            data = json.load(f)
           

        # Validate against the schema
        validate(instance=data, schema=schema)
       
        # Perform GitHub-specific validations
        validator = GitHubValidators()
        validator.validate_config(data)

        print("JSON is valid!")
        return data
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(2) #File not found
    except json.JSONDecodeError as e:
        # Detailed error reporting
        error_line = e.lineno
        error_col = e.colno
        error_message = e.msg
        
        print(f"Error: Invalid JSON format on line {error_line}, column {error_col}.")
        print(f"Details: {error_message}")
        sys.exit(3)  # Invalid JSON format
        # print(f"Error: Invalid JSON format. {e.msg}")
    except ValidationError as e:
        print(f"Schema Validation Error: {e.message}")
        sys.exit(4)  # Schema validation error
    except ValueError as e:
        print(f"Value Error during validation: {e}")
        sys.exit(5)  # GitHub-specific validation error
    except Exception as e:
        print(f"Unexpected error during validation: {e}")
        sys.exit(99)  # Unexpected error

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CLI JSON Validator")
    parser.add_argument("--show-sample", nargs="?", const=DEFAULT_SAMPLE_FILE, help="Path to the sample JSON file")
    parser.add_argument("--config", help="Path to the JSON config file to validate")
    args = parser.parse_args()
    try:
        csv_file_path="github_repo_data.csv"
        if args.show_sample and args.config:
            display_sample_json(args.show_sample)
            data=validate_json(args.config)
            username=data.get("username")
            repos=data.get("repositories")
            
            if username and repos:
                try:
                    fetch_github_repo_data(username, repos,csv_file_path)
                except Exception as e:
                    print(f"an error occured {e}")
                    sys.exit(99)
            else:
                print("Error: JSON file does not contain 'username' or 'repository'.")
                sys.exit(5)  # Missing required fields
        elif args.show_sample:
            display_sample_json(args.show_sample)
        elif args.config:
            data=validate_json(args.config)
            username=data.get("username")
            repos=data.get("repositories")
            if username and repos:
                try:
                    fetch_github_repo_data(username, repos,csv_file_path)
                except Exception as e:
                    print(f"an error occured {e}")
                    sys.exit(99)
            else:
                print("Error: JSON file does not contain 'username' or 'repository'.")
                sys.exit(5)  # Missing required fields
        else:
            print("Error: No arguments provided. Use --show-sample or --config.")
            sys.exit(1)  # No arguments provided

        

        
        
        
        print("Operation completed successfully.")
        sys.exit(0)  #success exit code
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(99)  # General unexpected error
