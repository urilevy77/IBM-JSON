import json
from json import JSONDecodeError

from jsonschema import Draft7Validator, exceptions, validate


def json_schema_validator(schema_str):
    try:
        generated_schema = json.loads(schema_str)
        try:
            Draft7Validator.check_schema(generated_schema)
            return True
        except exceptions.SchemaError:
            return False
    except JSONDecodeError:
        return False



def json_validator(json_instance, json_schema):
    try:
        generated_json = json.loads(json_instance)
        generated_schema = json.loads(json_schema)
        try:
            validate(generated_json, generated_schema)
            return True
        except exceptions.ValidationError:
            return False
    except JSONDecodeError:
        return False


