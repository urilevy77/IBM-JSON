import os
import random
import inflect
from dotenv import load_dotenv
from generators import *
from data_store import *
from validation import *
import sys

# Load environment variables from a .env file
load_dotenv()

# Set Hugging Face API token as an environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN


def receive_parameters():
    """Receives and validates command-line parameters."""
    try:
        number_of_jsons = int(sys.argv[1])
        story_structure_path = sys.argv[2]
        theme_path = sys.argv[3]
        errors_path = sys.argv[4]
        input_log_path = sys.argv[5]
        output_log_path = sys.argv[6]
        return number_of_jsons, story_structure_path, theme_path, errors_path, input_log_path, output_log_path
    except IndexError:
        print("Error: Not all parameters provided. You need to pass 4 parameters.")
        sys.exit(1)


def _generate_json_schema(structure, theme):
    """Generates a JSON schema using a given structure and theme."""
    schema = json_schema_generator(structure, theme)
    if json_schema_validator(schema):
        print("Valid json schema")
        return schema
    else:
        print(f"Invalid schema with theme: {theme} and structure: {structure}")
        return None


def _generate_json_instance(schema, index, num_to_string):
    """Generates a valid JSON instance based on a schema."""
    json_file = json_generator(schema, num_to_string.ordinal(index + 1))
    if json_validator(json_file, schema):
        print("Valid json instance")
        return json_file
    else:
        print("Invalid json instance")
        return None


def _generate_erroneous_json(schema, json_file, errors):
    """Generates erroneous JSON instances based on predefined errors."""
    for error in errors:
        desc, json_with_error = error_generator(json_file, error)
        if desc is not None:
            if json_validator(json_with_error, schema):
                print("No errors found in the erroneous json")
            else:
                print("Erroneous json created")
                save_json_details(schema, json_file, json_with_error, desc)


def _generate_user_model_interactions(input_log, output_log):
    """Generates user input and model output interactions based on erroneous JSONs."""
    counter = 0
    for arr_dict in JSON_DATA_DICTS:
        user_input = input_generator(arr_dict['json with error'])
        model_output = description_output_generator(arr_dict['error description'], arr_dict["json instance"])

        with_json_initial = random.randint(0, 1)
        if arr_dict['json with error'].startswith("```") or with_json_initial == 0:
            user_input_with_json_error = f"{user_input}\n{arr_dict['json with error']}"
        else:
            user_input_with_json_error = f"{user_input}\n```json\n{arr_dict['json with error']}\n```"

        model_output_with_json = f'{model_output}\n```json\n{arr_dict["json instance"]}\n```'

        INPUT_OUTPUT_DICT.append({"user input": user_input_with_json_error, "model output": model_output_with_json})

        with open(input_log, "a") as input_file:
            input_file.write(f"USER INPUT {counter + 1}:\n{INPUT_OUTPUT_DICT[counter]['user input']}\n\n")

        with open(output_log, "a") as output_file:
            output_file.write(f"MODEL OUTPUT {counter + 1}:\n{INPUT_OUTPUT_DICT[counter]['model output']}\n\n")

        counter += 1


def generation_flow(num_of_jsons, story_structure_path, theme_path, errors_path, input_log, output_log):
    """Handles the full data generation pipeline in a DFS manner."""
    num_to_string = inflect.engine()

    with open(story_structure_path, 'r') as structure_file:
        structures = [structure.strip() for structure in structure_file]

    with open(theme_path, 'r') as theme_file:
        themes = [theme.strip() for theme in theme_file]

    with open(errors_path, 'r') as error_file:
        errors = [error.strip() for error in error_file]

    for structure in structures:
        for theme in themes:
            schema = _generate_json_schema(structure, theme)
            if schema:
                for i in range(num_of_jsons):
                    json_file = _generate_json_instance(schema, i, num_to_string)
                    if json_file:
                        _generate_erroneous_json(schema, json_file, errors)

    _generate_user_model_interactions(input_log, output_log)


if __name__ == "__main__":
    NUM_OF_JSONS, STORY_STRUCTURE_PATH, THEME_PATH, ERRORS_PATH, INPUT_LOG, OUTPUT_LOG = receive_parameters()
    print("Started running")
    generation_flow(NUM_OF_JSONS, STORY_STRUCTURE_PATH, THEME_PATH, ERRORS_PATH, INPUT_LOG, OUTPUT_LOG)
