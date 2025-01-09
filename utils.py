# Global parameters
SCHEMAS_ARRAY = []
JSON_ARR_OF_ARR = []
ARRAY_OF_DICTS = []
INPUT_OUTPUT_DICT = []


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


def insert_all_to_dict(schema, json_instance, json_error, description):
    ARRAY_OF_DICTS.append({"json with error": json_error, "schema": schema, "json instance": json_instance,
                           "error description": description})

