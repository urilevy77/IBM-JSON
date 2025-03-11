# Global parameters
JSON_DATA_DICTS = []  # Stores dictionaries with schema, JSON instance, erroneous JSON and error details
INPUT_OUTPUT_DICT = []  # Reserved for mapping inputs and outputs

def save_json_details(schema, json_instance, erroneous_json, error_desc):
    """
        Adds schema, JSON instance, erroneous JSON, and error description as a dictionary into the global ARRAY_OF_DICTS.

        Args:
            schema (str): The JSON schema.
            json_instance (str): The JSON instance.
            erroneous_json (str): The erroneous JSON instance.
            error_desc (str): Description of the error.
        """
    JSON_DATA_DICTS.append({"json with error": erroneous_json,
                            "schema": schema,
                            "json instance": json_instance,
                            "error description": error_desc})
