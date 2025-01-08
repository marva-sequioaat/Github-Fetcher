import argparse
import json
import os
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class PathConfig:
    input_path: str
    output_path: str
    log_path: str

@dataclass
class Config:
    username: str
    serial_number: str
    repositories: List[str]
    paths: PathConfig
    timeout: int
    token: str

class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class ConfigValidator:
    @staticmethod
    def validate_username(username: str) -> None:
        if not isinstance(username, str):
            raise ConfigValidationError("Username must be a string")
        if not 3 <= len(username) <= 39:
            raise ConfigValidationError("Username length must be between 3 and 39 characters")
        if not username.replace("-", "").isalnum():
            raise ConfigValidationError("Username can only contain alphanumeric characters and hyphens")

    @staticmethod
    def validate_serial_number(serial: str) -> None:
        if not isinstance(serial, str):
            raise ConfigValidationError("Serial number must be a string")
        if not 8 <= len(serial) <= 12:
            raise ConfigValidationError("Serial number length must be between 8 and 12 characters")

    @staticmethod
    def validate_repositories(repos: List[str]) -> None:
        if not isinstance(repos, list):
            raise ConfigValidationError("Repositories must be a list")
        if not 1 <= len(repos) <= 10:
            raise ConfigValidationError("Number of repositories must be between 1 and 10")
        for repo in repos:
            if not isinstance(repo, str):
                raise ConfigValidationError("Repository names must be strings")

    @staticmethod
    def validate_paths(paths: PathConfig) -> None:
        # Validate input path exists
        if not os.path.exists(paths.input_path):
            raise ConfigValidationError(f"Input path does not exist: {paths.input_path}")

        # Validate output and log paths are writable
        for path_str in [paths.output_path, paths.log_path]:
            path = Path(path_str)
            if not path.parent.exists():
                try:
                    path.parent.mkdir(parents=True)
                except Exception as e:
                    raise ConfigValidationError(f"Cannot create directory for path: {path_str}. Error: {str(e)}")
            
            # Test if we can write to the directory
            try:
                test_file = path.parent / '.write_test'
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                raise ConfigValidationError(f"Directory not writable: {path.parent}. Error: {str(e)}")

    @staticmethod
    def validate_timeout(timeout: int) -> None:
        if not isinstance(timeout, int):
            raise ConfigValidationError("Timeout must be an integer")
        if not 10 <= timeout <= 60:
            raise ConfigValidationError("Timeout must be between 10 and 60 seconds")

    @staticmethod
    def validate_token(token: str) -> None:
        if not isinstance(token, str):
            raise ConfigValidationError("Token must be a string")
        if len(token) != 40:
            raise ConfigValidationError("Token length must be 40 characters")
        if not token.isalnum():
            raise ConfigValidationError("Token must contain only alphanumeric characters")

class ConfigProcessor:
    def __init__(self):
        self.parser = self._create_parser()
        self.validator = ConfigValidator()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='GitHub Repository Analysis Tool')
        parser.add_argument('--config', required=True, help='Path to config JSON file')
        parser.add_argument('--username', help='Override username from config file')
        parser.add_argument('--timeout', type=int, help='Override timeout from config file')
        return parser

    def read_config_file(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ConfigValidationError(f"Invalid JSON format in config file: {str(e)}")
        except FileNotFoundError:
            raise ConfigValidationError(f"Config file not found: {file_path}")

    def create_config(self, config_data: dict, cli_args: Optional[argparse.Namespace] = None) -> Config:
        # Override config values with CLI arguments if provided
        if cli_args:
            if cli_args.username:
                config_data['username'] = cli_args.username
            if cli_args.timeout:
                config_data['timeout'] = cli_args.timeout

        try:
            # Create PathConfig from nested dictionary
            paths = PathConfig(
                input_path=config_data['path']['input_path'],
                output_path=config_data['path']['output_path'],
                log_path=config_data['path']['log_path']
            )

            # Create main Config object
            config = Config(
                username=config_data['username'],
                serial_number=config_data['serial_number'],
                repositories=config_data['repositories'],
                paths=paths,
                timeout=config_data['timeout'],
                token=config_data['token']
            )

            # Validate all fields
            self.validate_config(config)
            return config

        except KeyError as e:
            raise ConfigValidationError(f"Missing required field in config: {str(e)}")

    def validate_config(self, config: Config) -> None:
        """Validate all fields in the config object."""
        self.validator.validate_username(config.username)
        self.validator.validate_serial_number(config.serial_number)
        self.validator.validate_repositories(config.repositories)
        self.validator.validate_paths(config.paths)
        self.validator.validate_timeout(config.timeout)
        self.validator.validate_token(config.token)

    def process(self) -> Config:
        """Main method to process command line arguments and config file."""
        args = self.parser.parse_args()
        config_data = self.read_config_file(args.config)
        return self.create_config(config_data, args)

def main():
    try:
        processor = ConfigProcessor()
        config = processor.process()
        print(f"Configuration loaded successfully for user: {config.username}")
        print(f"Will process {len(config.repositories)} repositories")
        # Config object is now ready to be used for GitHub API calls
        
    except ConfigValidationError as e:
        print(f"Configuration Error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()