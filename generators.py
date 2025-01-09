import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from config import MODEL  # Importing the configured model name
from prompts import *  # Importing prompt templates used for various generators

# Load environment variables from a .env file
load_dotenv()

# Set Hugging Face API token as an environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN


def invoke_with_seed(message):
    """
        Invokes the Hugging Face chat model with a predefined seed and parameters.

        Args:
            message (list): A list of chat messages (SystemMessage, HumanMessage, etc.)

        Returns:
            ChatHuggingFace response: The response from the chat model.
        """
    llm = HuggingFaceEndpoint(
        repo_id=MODEL,  # The Hugging Face model repository ID
        task="chat completion",
        max_new_tokens=500,
        seed=43,
        temperature=0.8
    )
    # Create a ChatHuggingFace instance
    chat_model = ChatHuggingFace(llm=llm)
    return chat_model.invoke(message)


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
        SystemMessage(content=SCHEMA_SYSTEM_PROMPT),  # System guidance for schema generation
        HumanMessage(content=VALID_SCHEMA_HUMAN_PROMPT),  # Instructions for valid schema
        AIMessage(content=SIMPLE_JSON_SCHEMA),  # Example JSON schema response
        HumanMessage(content=JSON_SCHEMA_HUMAN_PROMPT.format(theme=story_theme, structure=story_structure))
    ]

    response = invoke_with_seed(messages)
    schema_str = response.content
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
    message = [SystemMessage(content=JSON_GENERATOR_SYSTEM_PROMPT),  # System guidance for JSON generation
               HumanMessage(content=JSON_GENERATOR_HUMAN_PROMPT.format(schema=json_schema, number=json_num))]

    response = invoke_with_seed(message)
    json_instance = response.content
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
    message = [SystemMessage(content=JSON_ERROR_SYSTEM_PROMPT),  # System guidance for error generation
               HumanMessage(content=JSON_ERROR_HUMAN_PROMPT.format(json_instance=json_without_error, error=error_type))]

    response = invoke_with_seed(message)
    reply = response.content
    try:
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
    message = [SystemMessage(content=INPUT_GENERATOR_PROMPT),  # System guidance for input generation
               HumanMessage(content=f"The json with the error:{json_error}")]

    response = invoke_with_seed(message)
    reply = response.content
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
        HumanMessage(content=DESCRIPTION_OUTPUT_GENERATOR_PROMPT.format(description=description, json_instance=fixed_json))]

    response = invoke_with_seed(message)
    reply = response.content
    return reply
