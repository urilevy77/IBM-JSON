from jsonschema import Draft7Validator, exceptions,validate

def json_schema_validator(schema):
    try:
        Draft7Validator.check_schema(schema)
        print("The JSON schema is valid.")
    except exceptions.SchemaError as e:
        print("The JSON schema is invalid:")
        print(e)

def json_validator(json, schema):
    try:
        validate(json, schema)
        print("The JSON is valid.")
    except exceptions.SchemaError as e:
        print("The JSON is invalid:")
        print(e)