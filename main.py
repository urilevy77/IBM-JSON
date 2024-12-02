from huggingface_hub import InferenceClient
from config import STORY_STRUCTURE_PATH, THEME_PATH, ERRORS_PATH
from generators import error_generator, json_schema_generator, json_generator, input_generator
from utils import insert_schemas_to_arr, SCHEMAS_ARRAY, JSON_ARR_OF_ARR, insert_all_to_dict, \
    insert_json_arr_to_arr, DICT_FOR_INPUT
from validation import json_validator

if __name__ == "__main__":
    # client = InferenceClient()
    # # # for creating JSON schema out of story structure and theme
    # with open(STORY_STRUCTURE_PATH, 'r') as structure_file:
    #     for structure in structure_file:
    #         with open(THEME_PATH, 'r') as theme_file:
    #             for theme in theme_file:
    #                 schema = json_schema_generator(structure, theme)
    #                 insert_schemas_to_arr(schema)
    # seed_arr = 40
    # num_of_jsons = 2
    #
    # for schema in SCHEMAS_ARRAY:
    #     json_arr = []
    #     for i in range(num_of_jsons):
    #         json = json_generator(schema, seed_arr + i)
    #         json_arr.append(json)
    #     insert_json_arr_to_arr(json_arr)
    #
    # for i in range(len(SCHEMAS_ARRAY)):
    #     for json in JSON_ARR_OF_ARR[i]:
    #         with open(ERRORS_PATH, 'r') as error_file:
    #             for error in error_file:
    #                 desc, json_with_error = error_generator(json, error)
    #                 schema = SCHEMAS_ARRAY[i]
    #                 # checks if the description and the json with error is not None and
    #                 # if the json with error is not valid
    #                 if desc is not None and json_validator(json_with_error, schema) is False:
    #                     insert_all_to_dict(schema, json, json_with_error, desc)
    #
    # for key in DICT_FOR_INPUT.keys():
    #     input_generator(key)
    print("he")