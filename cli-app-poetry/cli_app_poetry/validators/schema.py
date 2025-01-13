"""

This schema defines the required structure and data types for the configuration file:
- username: GitHub username
- repositories: List of repository names to analyze

"""
schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "repositories": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 10
        }
    },
    "required": ["username", "repositories"]
}
