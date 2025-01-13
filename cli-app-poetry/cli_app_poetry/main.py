
"""
CLI tool for validating GitHub configuration JSON files.
Provides functionality to display sample JSON and validate config files
against a predefined schema and GitHub-specific requirements.
"""

import json
import os
from typing import Optional
from jsonschema import validate, ValidationError
from validators.schema import schema
from validators.github_validator import GitHubValidators
DEFAULT_SAMPLE_FILE = "sample.json"

def display_sample_json(file_path: str) -> None:
    """
    Displays the content of the sample JSON file.

    Args:
        file_path (str): Path to the sample JSON file.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = json.load(file)
                print("\nSample JSON File Content:")
                print(json.dumps(content, indent=4))
        else:
            print(f"Error: Sample JSON file '{file_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while displaying sample JSON: {e}")

def validate_json(file_path: str) -> None:
    """
    Validates a JSON file against schema and GitHub requirements.

    Args:
        file_path (str): Path to the JSON file to validate.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with open(file_path, "r") as f:
            data = json.load(f)  # Load JSON file

        # Validate against the schema
        validate(instance=data, schema=schema)

        # Perform GitHub-specific validations
        validator=GitHubValidators()
        validator.validate_config(data)

        print("JSON is valid!")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e.msg}")
    except ValidationError as e:
        print(f"Schema Validation Error: {e.message}")
    except ValueError as e:
        print(f"Value Error during validation: {e}")
    except Exception as e:
        print(f"Unexpected error during validation: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CLI JSON Validator")
    parser.add_argument("--show-sample", nargs="?", const=DEFAULT_SAMPLE_FILE,
                       help="Path to the sample JSON file")
    parser.add_argument("--config", help="Path to the JSON config file to validate", metavar="FILE")
    args = parser.parse_args()

    # Case 1: Both --show-sample and --config are provided
    if args.show_sample and args.config:
        display_sample_json(args.show_sample)
        validate_json(args.config)

    # Case 2: Only --show-sample is provided
    elif args.show_sample:
        display_sample_json(args.show_sample)

    # Case 3: Only --config is provided
    elif args.config:
        if args.config:
            validate_json(args.config)
        else:
            print("Error: No config file provided for validation. Use --config <FILE>.")

    # Case 4: No arguments provided
    else:
        print("Error: No arguments provided. Use --show-sample or --config.")