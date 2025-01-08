import json
import os
from jsonschema import validate, ValidationError
from github_validator import GitHubValidators
# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "repositories": {
            "type": "array",
            "items": {"type": "string"}
        },
        "path": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string"},
                "log_path": {"type": "string"}
            },
            "required": ["output_path", "log_path"]
        },
        "timeout": {"type": "number"},
        "metrics": {
            "type": "object",
            "properties": {
                "branches": {"type": "boolean"},
                "forks": {"type": "boolean"},
                "stars": {"type": "boolean"},
                "commits": {"type": "boolean"}
            },
            "required": ["branches", "forks", "stars", "commits"]
        }
    },
    "required": ["username", "repositories", "path", "metrics"]
}

# Function to load and validate JSON
def validate_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)  # Load JSON file
        validate(instance=data, schema=schema)  # Validate against schema
        # Then perform detailed GitHub-specific validations
        GitHubValidators.validate_config(data)
        print("JSON is valid!")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except ValidationError as e:
        print(f"Error: {e.message}")


# Entry point for the script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CLI JSON Validator")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    args = parser.parse_args()

    validate_json(args.config)
