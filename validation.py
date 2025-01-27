import json
from json import JSONDecodeError
from jsonschema import Draft7Validator, exceptions, validate


def json_schema_validator(schema_str):
    """
        Validates a JSON schema string to ensure it conforms to the JSON Schema Draft 7 specification.

        Args:
            schema_str (str): The JSON schema as a string.

        Returns:
            bool: True if the schema is valid, False otherwise.
        """
    try:
        # Parse the schema string into a Python dictionary
        generated_schema = json.loads(schema_str)
        try:
            # Check if the schema conforms to the Draft 7 standard
            Draft7Validator.check_schema(generated_schema)
            return True
        except exceptions.SchemaError:
            # Schema does not meet the required standards
            return False
    except JSONDecodeError:
        # Schema string is not a valid JSON
        return False


def json_validator(json_instance, json_schema):
    """
       Validates a JSON instance against a given JSON schema.

       Args:
           json_instance (str): The JSON instance as a string.
           json_schema (str): The JSON schema as a string.

       Returns:
           bool: True if the JSON instance conforms to the schema, False otherwise.
       """
    try:
        # Parse the JSON instance and schema strings into Python dictionaries
        generated_json = json.loads(json_instance)
        generated_schema = json.loads(json_schema)
        try:
            # Validate the JSON instance against the schema
            validate(generated_json, generated_schema)
            return True
        except exceptions.ValidationError:
            # JSON instance does not conform to the schema
            return False
    except JSONDecodeError:
        # JSON instance or schema string is not valid JSON
        return False
