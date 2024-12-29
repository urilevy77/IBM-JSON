import json
import os
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from config import MODEL
from prompts import *
from validation import json_schema_validator, json_validator

load_dotenv()
# Set Hugging Face API token as an environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN


def invoke_with_seed(message):
    llm = HuggingFaceEndpoint(
        repo_id=MODEL,  # You can choose a different model
        task="chat completion",
        max_new_tokens=500,
        seed=43,
        temperature=0.8
    )
    # Create a ChatHuggingFace instance
    chat_model = ChatHuggingFace(llm=llm)
    return chat_model.invoke(message)


def json_schema_generator(story_structure, story_theme):
    # Chat-style input with roles
    messages = [
        SystemMessage(content=SCHEMA_SYSTEM_PROMPT),
        HumanMessage(content=VALID_SCHEMA_PROMPT),
        AIMessage(content=SIMPLE_JSON_SCHEMA),
        HumanMessage(content=JSON_SCHEMA_PROMPT.format(theme=story_theme, structure=story_structure))
    ]

    response = invoke_with_seed(messages)
    schema_str = response.content
    return schema_str


def json_generator(json_schema, json_num):
    """Generates JSON instances from a given schema using chat completion."""
    message = [SystemMessage(content=JSON_GENERATOR_SYSTEM_PROMPT),
               HumanMessage(content=JSON_PROMPT.format(schema=json_schema, number=json_num))]

    response = invoke_with_seed(message)
    json_instance = response.content
    return json_instance


def error_generator(json_without_error, error_type):
    """Generates an invalid JSON instance by introducing a single error using chat completion."""
    message = [SystemMessage(content=JSON_ERROR_SYSTEM_PROMPT),
               HumanMessage(content=JSON_ERROR_PROMPT.format(json_instance=json_without_error, error=error_type))]

    response = invoke_with_seed(message)
    reply = response.content
    try:
        description, invalid_json_instance = reply.strip().split("\n\n", 1)
        return description, invalid_json_instance
    except ValueError:
        return None, None


def input_generator(json_error):
    message = [SystemMessage(content=INPUT_PROMPT),
               HumanMessage(content=f"The json with the error:{json_error}")]

    response = invoke_with_seed(message)
    reply = response.content
    return reply


def description_output_generator(description, fixed_json):
    message = [
        HumanMessage(content=DESCRIPTION_OUTPUT_PROMPT.format(description=description, json_instance=fixed_json))]

    response = invoke_with_seed(message)
    reply = response.content
    return reply
