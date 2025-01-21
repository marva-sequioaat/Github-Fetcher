from importlib.resources import files

DEFAULT_SAMPLE_FILE =  files('cli_app_poetry.validators').joinpath('sample.json')
GITHUB_API_URL = "https://api.github.com"
MAX_RETRIES=3
RETRY_DELAY=30