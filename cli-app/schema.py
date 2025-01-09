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