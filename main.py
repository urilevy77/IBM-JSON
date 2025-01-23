import os
import random
import inflect
from dotenv import load_dotenv
from jsonschema.exceptions import ValidationError
from config import STORY_STRUCTURE_PATH, THEME_PATH, ERRORS_PATH
from generators import *
from data_store import *
from validation import *
INPUT_OUTPUT_DICT = []  # Reserved for mapping inputs and outputs

# Load environment variables from a .env file
load_dotenv()

# Set Hugging Face API token as an environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN

if __name__ == "__main__":
    # Initialize the inflect engine to convert numbers to words (e.g., "1st", "2nd")
    num_to_string = inflect.engine()

    # Number of JSON instances to generate per schema
    num_of_jsons = 2

    # Load themes and errors into memory once at the beginning
    with open(THEME_PATH, 'r') as theme_file:
        themes = [theme.strip() for theme in theme_file]

    with open(ERRORS_PATH, 'r') as error_file:
        errors = [error.strip() for error in error_file]

    # Step 1: Generate JSON schemas using story structures and themes
    # Read the story structure and theme files to create schemas
    with open(STORY_STRUCTURE_PATH, 'r') as structure_file:
        for structure in structure_file:
            for theme in themes:
                # Generate a JSON schema for each combination of structure and theme
                generated_schema = json_schema_generator(structure, theme.replace("\n", ""))

                # Validate the schema and add it to the global array if valid
                if json_schema_validator(generated_schema):
                    save_schema(generated_schema)

    # Step 2: Generate JSON instances for each valid schema
    # Iterate through each schema in the global schemas array
    for json_schema in SCHEMAS_ARRAY:
        json_arr = []

        # Generate multiple JSON instances per schema
        for i in range(num_of_jsons):
            json_file = json_generator(json_schema, num_to_string.ordinal(i + 1))

            # Validate the generated JSON and add it to the array if valid
            if json_validator(json_file, json_schema):
                json_arr.append(json_file)

        # Store the array of JSON instances in the global JSON_ARR_OF_ARR
        save_jsons(json_arr)

    # Step 3: Generate errors for each JSON instance and validate them
    # Iterate through the schemas and corresponding JSON arrays
    for i in range(len(SCHEMAS_ARRAY)):
        for json_file in JSON_ARR_OF_ARR[i]:
            if json_file is not None:
                # Generate errors for each type specified in the errors file
                for error in errors:
                    desc, json_with_error = error_generator(json_file, error)
                    schema = SCHEMAS_ARRAY[i]

                    # Validate the generated erroneous JSON and add it to the global dictionary if invalid
                    if desc is not None:
                        try:
                            json_instance_error = json.loads(json_with_error)
                            validate(json_with_error, schema)  # Ensure the error makes the JSON invalid
                        except (JSONDecodeError, ValidationError, TypeError) as e:
                            save_json_details(schema, json_file, json_with_error, desc)

    # Step 4: Generate user inputs and model outputs for each error
    counter = 0  # Counter for printing user input and model output pairs

    for arr_dict in JSON_DATA_DICTS:
        # Generate user input based on the erroneous JSON
        user_input = input_generator(arr_dict['json with error'])

        # Generate the model's output based on the error description and original JSON
        model_output = description_output_generator(arr_dict['error description'], arr_dict["json instance"])

        # Randomize whether the erroneous JSON is prefixed with code block formatting
        with_json_initial = random.randint(0, 1)
        if arr_dict['json with error'].startswith("```") or with_json_initial == 0:
            user_input_with_json_error = f"{user_input}\n{arr_dict['json with error']}"
        else:
            user_input_with_json_error = f"{user_input}\n```json\n{arr_dict['json with error']}\n```"

        # Format the model output to include the corrected JSON
        model_output_with_json = f'{model_output}\n```json\n{arr_dict["json instance"]}\n```'

        # Append the user input and model output pair to the global INPUT_OUTPUT_DICT
        INPUT_OUTPUT_DICT.append(
            {"user input": user_input_with_json_error,
             "model output": model_output_with_json})

        # Print the user input for debugging
        print(f"{counter})USER INPUT: {INPUT_OUTPUT_DICT[counter]['user input']}")
        print(f"MODEL OUTPUT: {INPUT_OUTPUT_DICT[counter]['model output']}")
        counter += 1
