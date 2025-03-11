import json

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from config import MODEL  # Importing the configured model name
from prompts import *  # Importing prompt templates used for various generators
from typing import Optional
import yaml
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# Load the YAML file
def _load_prompts(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Load prompts
prompts = _load_prompts("prompts.yaml")


def _invoke_messages(messages: list, seed: Optional[int] = 43):
    """
        Invokes the Hugging Face chat model with a predefined seed and parameters.

        Args:
            messages (list): A list of chat messages (SystemMessage, HumanMessage, etc.)
            seed (int) : Optional integer for model seed
        Returns:
            ChatHuggingFace response: The response from the chat model.
        """
    llm = HuggingFaceEndpoint(
        repo_id=MODEL,
        task="chat completion",
        max_new_tokens=500,
        seed=seed,
        temperature=0.8
    )
    # Create a ChatHuggingFace instance
    chat_model = ChatHuggingFace(llm=llm)
    return chat_model.invoke(messages).content


def json_schema_generator(story_structure, story_theme):
    """
       Generates a JSON schema based on the given story structure and theme.

       Args:
           story_structure (str): The structure of the story (e.g., "narrative", "dialogue").
           story_theme (str): The theme of the story (e.g., "adventure", "science fiction").

       Returns:
           str: The generated JSON schema as a string.
       """
    messages = [
        SystemMessage(content=prompts["schema_system_prompt"]),
        HumanMessage(content=prompts["json_schema_human_prompt"]["template"].format(
            theme=story_theme, structure=story_structure)),
    ]
    schema_str = _invoke_messages(messages)
    return schema_str


def json_generator(json_schema, json_num):
    """
        Generates JSON instance from a given schema.

        Args:
            json_schema (str): The schema used to generate JSON instance.
            json_num (str): Number of JSON instance to generate (e.g., "1st", "2nd").

        Returns:
            str: Generated JSON instance as a single string.
        """
    message = [
        HumanMessage(content=prompts["json_generator_human_prompt"]["template"].format(
            schema=json_schema, number=json_num))
    ]

    json_instance = _invoke_messages(message)
    return json_instance


def error_generator(json_without_error, error_type):
    """
    Generates an invalid JSON instance by introducing a specified error.

    Args:
        json_without_error (str): A valid JSON instance as a string.
        error_type (str): The type of error to introduce (e.g., "missing field", "wrong format").

    Returns:
        tuple: Description of the error and the invalid JSON instance.
    """
    # Define the expected structure of the output
    response_schemas = [
        ResponseSchema(name="description", description="A brief description of the error (one sentence)."),
        ResponseSchema(name="invalid_json", description="The erroneous JSON instance.")
    ]

    # Create the output parser with the defined response schemas
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # Construct the system and human messages
    message = [
        SystemMessage(content=prompts["json_error_system_prompt"]),
        HumanMessage(content=prompts["json_error_human_prompt"]["template"].format(
            json_instance=json_without_error, error=error_type)),
    ]

    # Invoke the model and parse the output
    reply = _invoke_messages(message)
    try:
       # # Use the output parser to parse the response
        #parsed_output = output_parser.parse(reply)
        #if isinstance(parsed_output["invalid_json"], dict):
            #parsed_output["invalid_json"] = json.dumps(parsed_output["invalid_json"], indent=4)
        #return parsed_output["description"], parsed_output["invalid_json"]
    #except Exception as e:
       #print(f"Error parsing model response: {e}")
        #return None, None
        description, invalid_json_instance = reply.strip().split("\n\n", 1)
        return description, invalid_json_instance
    except ValueError:
        return None, None  # Handle unexpected response format


def input_generator(json_error):
    """
       Generates input for fixing the JSON error.

       Args:
           json_error (str): The erroneous JSON instance.

       Returns:
           str: Suggested input or approach to fix the JSON error.
       """
    message = [
        SystemMessage(content=prompts["input_generator_prompt"]),
        HumanMessage(content=f"The json with the error:{json_error}"),
    ]

    reply = _invoke_messages(message)
    return reply


def description_output_generator(description, fixed_json):
    """
        Generates a description of the fixed JSON and outputs it.

        Args:
            description (str): Description of the error.
            fixed_json (str): The corrected JSON instance.

        Returns:
            str: A comprehensive description of the fixed JSON.
        """
    message = [
        HumanMessage(content=prompts["description_output_generator_prompt"]["template"].format(
            description=description, json_instance=fixed_json))
    ]

    reply = _invoke_messages(message)
    return reply
