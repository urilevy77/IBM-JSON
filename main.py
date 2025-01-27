import os
import random
import inflect
from dotenv import load_dotenv
from jsonschema.exceptions import ValidationError
from config import *
from generators import *
from data_store import *
from validation import *


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
    count_schema_error=0
    count_json_error=0

    # Step 1: Generate JSON schemas using story structures and themes
    # Read the story structure and theme files to create schemas
    with open(STORY_STRUCTURE_PATH, 'r') as structure_file:
        for structure in structure_file:
            for theme in themes:
                # Generate a JSON schema for each combination of structure and theme
                generated_schema = json_schema_generator(structure, theme.replace("\n", ""))

                # Validate the schema and add it to the global array if valid
                if json_schema_validator(generated_schema):
                    # Step 2: Generate JSON instances for each valid schema
                    for i in range(num_of_jsons):
                        json_file = json_generator(generated_schema, num_to_string.ordinal(i + 1))
                        if json_validator(json_file, generated_schema):
                            # Step 3: Generate errors for each JSON instance and validate them
                            for error in errors:
                                desc, json_with_error = error_generator(json_file, error)
                                # Validate the generated erroneous JSON and add it to the global dictionary if invalid
                                if desc is not None:
                                    try:
                                        json_instance_error = json.loads(json_with_error)
                                        validate(json_with_error, json.loads(generated_schema))  # Ensure the error makes the JSON invalid
                                    except (JSONDecodeError, ValidationError, TypeError) as e:
                                        save_json_details(generated_schema, json_file, json_with_error, desc)
                        else:
                            count_json_error+=1
                else:
                    count_schema_error+=1
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

        # # Print the user input for debugging
        # print(f"USER INPUT {counter + 1}: {INPUT_OUTPUT_DICT[counter]['user input']}")
        # print(f"MODEL OUTPUT {counter + 1}: {INPUT_OUTPUT_DICT[counter]['model output']}")

        # Open the file in append mode to save the data
        with open(INPUT_LOG, "a") as input_file:
            # Write the user input and model output to the file
            input_file.write(f"USER INPUT {counter + 1}:\n{INPUT_OUTPUT_DICT[counter]['user input']}\n")
            input_file.write("\n")  # Add a blank line for readability

        with open(OUTPUT_LOG, "a") as output_file:
            output_file.write(f"MODEL OUTPUT {counter + 1}:\n{INPUT_OUTPUT_DICT[counter]['model output']}\n")
            output_file.write("\n")  # Add a blank line for readability
        counter += 1
    print(count_schema_error)
    print(count_json_error)