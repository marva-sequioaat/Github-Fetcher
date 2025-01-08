# import json
# import os
# from jsonschema import validate, ValidationError
# from github_validator import GitHubValidators
# # Define the JSON schema
# schema = {
#     "type": "object",
#     "properties": {
#         "username": {"type": "string"},
#         "repositories": {
#             "type": "array",
#             "items": {"type": "string"}
#         },
#         "path": {
#             "type": "object",
#             "properties": {
#                 "output_path": {"type": "string"},
#                 "log_path": {"type": "string"}
#             },
#             "required": ["output_path", "log_path"]
#         },
#         "timeout": {"type": "number"},
#         "metrics": {
#             "type": "object",
#             "properties": {
#                 "branches": {"type": "boolean"},
#                 "forks": {"type": "boolean"},
#                 "stars": {"type": "boolean"},
#                 "commits": {"type": "boolean"}
#             },
#             "required": ["branches", "forks", "stars", "commits"]
#         }
#     },
#     "required": ["username", "repositories", "path", "metrics"]
# }

# #Function to display sample JSON to the user
# def display_sample_json(file_path):
#     """Displays the content of the sample JSON file."""
#     if os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             content = json.load(file)
#             print("\nSample JSON File Content:")
#             print(json.dumps(content, indent=4))
#     else:
#         print("Sample JSON file not found.")


# # Function to load and validate JSON
# def validate_json(file_path):
#     try:
#         with open(file_path, "r") as f:
#             data = json.load(f)  # Load JSON file
#         validate(instance=data, schema=schema)  # Validate against schema
#         # Then perform detailed GitHub-specific validations
#         GitHubValidators.validate_config(data)
#         print("JSON is valid!")
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#     except json.JSONDecodeError:
#         print("Error: Invalid JSON format.")
#     except ValidationError as e:
#         print(f"Error: {e.message}")


# # Entry point for the script
# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="CLI JSON Validator")
#     parser.add_argument("--show-sample", action="store_true", help="Display the sample JSON file")
#     parser.add_argument("--config", required=True, help="Path to the JSON config file")
#     parser.add_argument(
#         "--show-sample",
#         action="store_true",
#         help="Display a sample JSON configuration"
#     )
#     args = parser.parse_args()
#     # Interactive flow
#     if args.show_sample:
#         display_sample_json("sample_config.json")
#     else:
#         user_response = input("Do you want to see a sample JSON file? (yes/no): ").strip().lower()
#         if user_response in ["yes", "y"]:
#             display_sample_json("sample_config.json")
#         else:
#             print("Okay, proceeding without showing the sample JSON file.")
#     else:
#         if not args.config:
#             args.config=input("Please enter your input file path")
#     validate_json(args.config)


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

# Function to display sample JSON to the user
def display_sample_json(file_path):
    """Displays the content of the sample JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = json.load(file)
            print("\nSample JSON File Content:")
            print(json.dumps(content, indent=4))
    else:
        print("Sample JSON file not found.")

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
    parser.add_argument("--show-sample", action="store_true", help="Display the sample JSON file")
    parser.add_argument("--config", help="Path to the JSON config file")
    args = parser.parse_args()

    # Ask if the user wants to see a sample JSON
    user_response = input("Do you want to see a sample JSON file? (yes/no): ").strip().lower()
    if user_response in ["yes", "y"]:
        display_sample_json("sample_config.json")
    
    # Ask for the configuration file path if not provided via CLI
    config_file = args.config
    if not config_file:
        config_file = input("Please enter the path to your JSON config file: ").strip()

    # Validate the JSON configuration file
    if config_file:
        validate_json(config_file)
    else:
        print("Error: No config file provided.")
