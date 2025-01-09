# Global parameters
SCHEMAS_ARRAY = []  # Stores all generated JSON schemas
JSON_ARR_OF_ARR = []  # Stores two-dimensional arrays of JSON instances
JSON_DATA_DICTS = []  # Stores dictionaries with schema, JSON instance, erroneous JSON and error details
INPUT_OUTPUT_DICT = []


def insert_schemas_to_arr(schema):
    """
        Inserts a JSON schema into the global SCHEMAS_ARRAY.

        Args:
            schema (str): A JSON schema to be added to the global array.
        """
    if schema is not None:
        SCHEMAS_ARRAY.append(schema)


def insert_json_arr_to_arr(json_arr):
    """
    Inserts a list of JSON instances into the global JSON_ARR_OF_ARR.

    Args:
        json_arr (list): A list of JSON instances to be added to the global array.
    """
    JSON_ARR_OF_ARR.append(json_arr)


def insert_all_to_dict(schema, json_instance, erroneous_json, error_desc):
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

