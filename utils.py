from generators import json_generator

SCHEMAS_ARRAY = []
JSON_ARR_OF_ARR = []
DICT_FOR_INPUT = {}


def insert_schemas_to_arr(schema):
    """
    insert a json_ schema that we created into a global array of schemas

    """
    if schema is not None:
        SCHEMAS_ARRAY.append(schema)


def insert_json_arr_to_arr(json_arr):
    """
     insert to the global two-dimensional array of jsons

    """
    JSON_ARR_OF_ARR.append(json_arr)


def insert_all_to_dict(schema, json, json_error, description):
    DICT_FOR_INPUT[json_error] = [schema, json, description]
