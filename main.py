from huggingface_hub import InferenceClient
import json

from config import JSON_PATH, JSON_SCHEMA_PATH, STORY_STRUCTURE_PATH, THEME_PATH
from generators import json_schema_generator, json_generator, error_generator
from validation import json_schema_validator, json_validator
from utils import read_url

if __name__ == "__main__":
    client = InferenceClient()
    # # for creating JSON schema out of story structure and theme
    # with open(STORY_STRUCTURE_PATH, 'r') as structure_file:
    #     for structure in structure_file:
    #         with open(THEME_PATH, 'r') as theme_file:
    #             for theme in theme_file:
    #                 json_schema_generator(structure, theme)
    #
    # # creating JSONs out of JSON schema
    # with open(JSON_SCHEMA_PATH, 'r') as json_schema_file:
    #     schema = json_schema_file.read()
    #     json_generator(schema)

    # # creating errors on JSONs
    with open(JSON_PATH, 'r') as json_file:
        json = json_file.read()
        error_generator(json)
    # print(type(read_url()))
    # with open(JSON_PATH) as file:
    #     json_try = (file.read())
    # with open(JSON_SCHEMA_PATH) as schema_file:
    #     schema_try = schema_file.read()
    # #print(json_try)
    # #print(schema_try)
    # validate(instance=json_try, schema=schema_try)
    # schema = {
    #     "$schema": "http://json-schema.org/draft-07/schema#",
    #     "type": "object",
    #     "properties": {
    #         "name": {"type": "string"},
    #         "age": {"type": "integer", "minimum": 0},
    #         "email": {"type": "string", "format": "email"}
    #     },
    #     "required": ["name", "age"]
    # }
    # json_schema_validator(schema)
# JSON_SCHEMA_PATH = "JSONschema"
# JSON_PATH = "JSON"
    #json_validator(json.loads(json_try), json.loads(schema_try))