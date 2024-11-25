import json
from config import MODEL
from prompts import *
from validation import json_schema_validator
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
    generated_schema = json.loads(schema_str)
    json_schema_validator(generated_schema)


def json_generator(json_schema):
    """Generates JSON instances from a given schema using chat completion."""
    chat_input = [
        {
            "role": "system",
            "content": JSON_GENERATOR_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"This is a JSON schema: {json_schema}"
        },
        {
            "role": "user",
            "content": f"{JSON_PROMPT}"
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
    json_instances = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(json_instances)


# def json_generator(json_schema):
#     response = CLIENT.text_generation(
#         prompt=f"{JSON_PROMPT} {json_schema}",
#         model=MODEL,
#         temperature=0.8,
#         max_new_tokens=500,
#         seed=44,
#         return_full_text=False,
#     )
#     print(response)

def error_generator(json_without_error):
    """Generates an invalid JSON instance by introducing a single error using chat completion."""
    chat_input = [
        {
            "role": "system",
            "content": JSON_ERROR_SYSTEM_PROMPT
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
    invalid_json_instance = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(invalid_json_instance)

# def error_generator(json_without_error):
#     response = CLIENT.text_generation(
#         prompt=f"{JSON_ERROR_PROMPT} {json_without_error}",
#         model=MODEL,
#         temperature=0.8,
#         max_new_tokens=500,
#         seed=44,
#         return_full_text=False,
#     )
#     print(response)

# \n\n{json.dumps(json_without_error, indent=2)}
