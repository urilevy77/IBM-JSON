import json
import random
import inflect
from json import JSONDecodeError
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from config import STORY_STRUCTURE_PATH, THEME_PATH, ERRORS_PATH
from generators import *
from data_store import *
from validation import json_validator, json_schema_validator


if __name__ == "__main__":
    # Create an inflect engine instance
    num_to_string = inflect.engine()
    num_of_jsons = 2
    # creating JSON schema from story structure and theme, and insert to a array
    with open(STORY_STRUCTURE_PATH, 'r') as structure_file:
        for structure in structure_file:
            with open(THEME_PATH, 'r') as theme_file:
                for theme in theme_file:
                    generated_schema = json_schema_generator(structure, theme.replace("\n", ""))
                    if json_schema_validator(generated_schema):
                        insert_schemas_to_arr(generated_schema)

    # iterate on the schmas array and create multiple jsons, and insert to an array of array of jsons
    for json_schema in SCHEMAS_ARRAY:
        json_arr = []
        for i in range(num_of_jsons):
            json_file = json_generator(json_schema, num_to_string.ordinal(i + 1))
            if json_validator(json_file, json_schema):
                json_arr.append(json_file)
        insert_json_arr_to_arr(json_arr)

    # iterate on the schemas array and the json array and create for each json an error
    for i in range(len(SCHEMAS_ARRAY)):
        for json_file in JSON_ARR_OF_ARR[i]:
            with open(ERRORS_PATH, 'r') as error_file:
                if json_file is not None:

                    print(f"{i + 1} is valid")
                    for error in error_file:
                        desc, json_with_error = error_generator(json_file, error)
                        schema = SCHEMAS_ARRAY[i]

                        # checks if the description and the json with error is not None and insert to a dictionary

                        if desc is not None:
                            try:
                                json_instance_error = json.loads(json_with_error)
                                validate(json_with_error, schema)
                            except (JSONDecodeError, ValidationError, TypeError) as e:
                                insert_all_to_dict(schema, json_file, json_with_error, desc)
                else:
                    print(f"{i + 1} not valid")
    # # creating input for the user ond output of the model and insert it to a dictionary
    # k its for printing the arrays inside the dictionary
    k = 0

    for arr_dict in JSON_DATA_DICTS:
        user_input = input_generator(arr_dict['json with error'])
        model_output = description_output_generator(arr_dict['error description'], arr_dict["json instance"])
        with_json_initial = random.randint(0, 1)
        if arr_dict['json with error'].startswith("```") or with_json_initial == 0:
            user_input_with_json_error = f"{user_input}\n{arr_dict['json with error']}"
        else:
            user_input_with_json_error = f"{user_input}\n```json\n{arr_dict['json with error']}\n```"

        model_output_with_json = f'{model_output}\n```json\n{arr_dict["json instance"]}\n```'

        INPUT_OUTPUT_DICT.append(
            {"user input": user_input_with_json_error,
             "model output": model_output_with_json})

        print(f"{k})USER INPUT: {INPUT_OUTPUT_DICT[k]['user input']}")
        # print(f"MODEL OUTPUT: {INPUT_OUTPUT_DICT[k]['model output']}")
        k += 1
