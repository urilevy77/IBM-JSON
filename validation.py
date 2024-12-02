from jsonschema import Draft7Validator, exceptions, validate


def json_schema_validator(schema):
    try:
        Draft7Validator.check_schema(schema)
        return True
    except exceptions.SchemaError as e:
        return False


def json_validator(json, schema):
    try:
        validate(json, schema)
        return True
    except exceptions.ValidationError as e:
        return False

