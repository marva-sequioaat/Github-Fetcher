import json
import os
from jsonschema import validate, ValidationError

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
# def validate_json(file_path):
#     try:
#         with open(file_path, "r") as f:
#             data = json.load(f)  # Load JSON file
#         validate(instance=data, schema=schema)  # Validate against schema
#         print("JSON is valid!")
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#     except json.JSONDecodeError:
#         print("Error: Invalid JSON format.")
#     except ValidationError as e:
#         print(f"Error: {e.message}")

def validate_json(file_path):
    try:
        # First check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            print(f"Current working directory: {os.getcwd()}")
            return

        # Try to read the file contents
        with open(file_path, "r") as f:
            file_content = f.read()
            print("File content:", file_content)  # Debug print
            
            try:
                data = json.loads(file_content)  # Load JSON file
            except json.JSONDecodeError as json_err:
                print(f"JSON Decode Error: {str(json_err)}")
                print(f"Error occurred at line {json_err.lineno}, column {json_err.colno}")
                return

        # Validate against schema
        validate(instance=data, schema=schema)
        print("JSON is valid!")
        return data

    except ValidationError as e:
        print(f"Schema Validation Error: {e.message}")
        print(f"Failed at path: {' -> '.join(str(p) for p in e.path)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

# Entry point for the script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CLI JSON Validator")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    args = parser.parse_args()

    validate_json(args.config)
