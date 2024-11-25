import requests

def read_url():
    """Reads the JSON Schema Draft-07 meta-schema from its URL."""
    SCHEMA_FOR_JSON_SCHEMA = "http://json-schema.org/draft-07/schema#"
    response = requests.get(SCHEMA_FOR_JSON_SCHEMA)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Failed to retrieve schema: {response.status_code}")
