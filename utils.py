import requests

from config import STORY_STRUCTURE_PATH, THEME_PATH
from generators import json_schema_generator, json_generator

SCHEMAS_ARRAY = []
JSON_ARR_OF_ARR = []


def insert_schemas_to_arr(structure,theme):
    """
    insert a json_ schema that we created into a global array of schemas

    """
    schema = json_schema_generator(structure, theme)
    if schema is not None:
        SCHEMAS_ARRAY.append(schema)


def insert_json_to_arr(schema, num_of_jsons):
    """
    create jsons of a schema and insert to arr, and then insert to the global two-dimensional array of jsons
    :param schema: schema
    :param num_of_jsons: number of jsons we want to generate from the schema

    """
    seed_arr = 40
    json_arr = []
    for i in range(num_of_jsons):
        json = json_generator(schema, seed_arr+i)
        if json is not None:
            json_arr.append(json)
    JSON_ARR_OF_ARR.append(json_arr)


def read_url():
    """Reads the JSON Schema Draft-07 meta-schema from its URL."""
    SCHEMA_FOR_JSON_SCHEMA = "http://json-schema.org/draft-07/schema#"
    response = requests.get(SCHEMA_FOR_JSON_SCHEMA)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Failed to retrieve schema: {response.status_code}")
