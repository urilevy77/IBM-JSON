import json
from json.decoder import JSONDecodeError

from config import MODEL
from prompts import *
from validation import json_schema_validator, json_validator
from huggingface_hub import InferenceClient

CLIENT = InferenceClient()


def json_schema_generator(story_structure, story_theme):
    # Chat-style input with roles
    chat_input = [
        {
            "role": "system",
            "content": SCHEMA_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"{VALID_SCHEMA_PROMPT}"
        },
        {
            "role": "assistant",
            "content": """{
              "$schema": "http://json-schema.org/draft-07/schema#",
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "age": { "type": "integer", "minimum": 0 },
                "email": { "type": "string", "format": "email" }
              },
              "required": ["name", "age"]
            }"""
        },
        {
            "role": "user",
            "content": f"{story_structure}  {JSON_SCHEMA_PROMPT} {story_theme}"
        }
    ]

    # Call the chat completion API
    second_response = CLIENT.chat_completion(
        messages=chat_input,
        model=MODEL,
        temperature=0.8,
        max_tokens=500,
        seed=42,
    )

    # Extract and print the assistant's reply
    schema_str = second_response.get("choices", [{}])[0].get("message", {}).get("content", "")
    try:
        generated_schema = json.loads(schema_str)
        if json_schema_validator(generated_schema):
            return schema_str
    except JSONDecodeError as e:
        return None


def json_generator(json_schema, json_seed):
    """Generates JSON instances from a given schema using chat completion."""
    chat_input = [
        {
            "role": "system",
            "content": JSON_GENERATOR_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"This is a JSON schema:\n {json_schema}\n {JSON_PROMPT}"
        }
    ]

    # Call the chat completion API
    response = CLIENT.chat_completion(
        messages=chat_input,
        model=MODEL,
        temperature=0.8,
        max_tokens=500,
        seed=json_seed,
    )

    # Extract and print the assistant's reply
    json_instance = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    try:
        generated_json = json.loads(json_instance)
        generated_schema = json.loads(json_schema)
        if json_validator(generated_json, generated_schema):
            return json_instance
    except JSONDecodeError as e:
        return None


def error_generator(json_without_error, error_type):
    """Generates an invalid JSON instance by introducing a single error using chat completion."""
    chat_input = [
        {
            "role": "system",
            "content": f"{JSON_ERROR_SYSTEM_PROMPT} {error_type}"
        },
        {
            "role": "user",
            "content": f"{JSON_ERROR_PROMPT} {json_without_error} "
        }
    ]

    # Call the chat completion API
    response = CLIENT.chat_completion(
        messages=chat_input,
        model=MODEL,
        temperature=0.8,
        max_tokens=500,
        seed=44,
    )

    # Extract and print the assistant's reply
    reply = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    # Split the reply into description and JSON
    try:
        description, invalid_json_instance = reply.strip().split("\n\n", 1)
        return description, invalid_json_instance
    except ValueError:
        return None, None


def input_generator(json_error):
    chat_input = [
        {
            "role": "system",
            "content": f"{INPUT_PROMPT}"
        },
        {
            "role": "user",
            "content": f"The json with the error:{json_error}"
        }
    ]

    # Call the chat completion API
    response = CLIENT.chat_completion(
        messages=chat_input,
        model=MODEL,
        temperature=0.8,
        max_tokens=500,
        seed=44,
    )
    reply = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return reply


def description_output_generator(description, fixed_json):
    chat_input = [

        {
            "role": "user",
            "content": f"{DESCRIPTION_OUTPUT_PROMPT} \n this is the error description:{description} \n and this is "
                       f"the corrected json: {fixed_json}"
        }
    ]

    # Call the chat completion API
    response = CLIENT.chat_completion(
        messages=chat_input,
        model=MODEL,
        temperature=0.8,
        max_tokens=500,
        seed=44,
    )
    reply = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return reply